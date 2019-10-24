package com.unbabel.event

import java.io.FileNotFoundException
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

import com.fasterxml.jackson.core.io.JsonEOFException
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.exc.{MismatchedInputException, ValueInstantiationException}
import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}
import com.unbabel.config.Constants._
import com.unbabel.exception.InvalidEventException

import scala.io.Source

object EventHandler {

  private val mapper = new ObjectMapper() with ScalaObjectMapper
  mapper.registerModule(DefaultScalaModule)

  /** Returns a sequence of [[com.unbabel.event.Event]] from a given JSON file
    *
    * @param filename Name of the file
    * @throws com.unbabel.exception.InvalidEventException Returned when there are problems parsing the events
    * @throws java.io.FileNotFoundException Returned when the file can  not be found
    * @return List of [[com.unbabel.event.Event]]
    */
  @throws(classOf[InvalidEventException])
  @throws(classOf[FileNotFoundException])
  def readEvents(filename:String) :  List[Event]  = {
    try {
      val jsonFile = Source.fromFile(filename)

      // Materializes each line of the JSON file in an Event.
      // Exceptions thrown in case the file does not exist or whose content is not valid.
      jsonFile
        .getLines()
        .map( line => mapper.readValue[Event](line))
        .toList

    } catch {
      case ex: FileNotFoundException =>
        throw ex

      case ex @ (
          _ : ValueInstantiationException |
          _ : JsonEOFException |
          _ : MismatchedInputException ) =>
        throw new InvalidEventException("Unable to parse events from input file. " + ex.getMessage)
    }
  }

  /** Generates a minute-by-minute sliding window between the min and max timestamp of the input events.
    * To each position is attached the events that happened in the previous N minutes.
    *
    * @param windowSize Size of the window
    * @param events List of events
    * @return Minute-by-minute sliding window of events
    */
  def slidingWindowByTimestamp(windowSize: Long, events : List[Event]) : Seq[(LocalDateTime, List[Event])]  = {

    if(windowSize < 0 || events.isEmpty) return Seq()

    // Sort the events by timestamp
    val orderedEvents = events.sortWith(_.timestamp < _.timestamp)
    val earliest = orderedEvents.head.timestampDateTime.truncatedTo(ChronoUnit.MINUTES)
    val latest = orderedEvents.takeRight(1).head.timestampDateTime.truncatedTo(ChronoUnit.MINUTES)

    // Create a sequence of minutes between the earliest event and the latest event
    (0.longValue() to earliest.until(latest, ChronoUnit.MINUTES) + 1)
      .map(i => earliest.plusMinutes(i))
      .map(datetime => {
        // For each minute, attach a list of events happening within the defined windowSize
        datetime -> events.filter(e => {
          val diff = e.timestampDateTime.until(datetime, ChronoUnit.MILLIS)
          diff > 0 && diff < windowSize * MILLIS_PER_MIN
        })
      })
  }

  /** Calculates a moving average of the translation delivery time
    *
    * @param slidingWindow Input list of events distributed by a sliding window
    */
  def calculateAverageDeliveryTime(slidingWindow: Seq[(LocalDateTime, List[Event])]) : Seq[AvgDeliveryTime] = {

    val formatter = DateTimeFormatter.ofPattern(OUTPUTDATEFORMAT)
    slidingWindow
      .map(list => {
        val date = list._1.format(formatter)
        val avg = list._2.map(_.duration).sum/list._2.length.toDouble

        AvgDeliveryTime(date, if(avg.isNaN) 0 else avg )
      })

  }

  /** Prints sliding window of Average Delivery Times
    *
    * @param out None
    */
  def printAverageDeliveryTime(out : Seq[AvgDeliveryTime]) : Unit = {
    out.foreach(value => println(mapper.writeValueAsString(value)))
  }

}