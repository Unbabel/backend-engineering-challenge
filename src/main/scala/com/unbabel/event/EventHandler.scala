package com.unbabel.event

import java.io.FileNotFoundException
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.core.io.JsonEOFException
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.exc.{MismatchedInputException, ValueInstantiationException}
import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}
import com.unbabel.config.Constants._

import scala.io.Source

object EventHandler {

  private val mapper = new ObjectMapper() with ScalaObjectMapper
  mapper.registerModule(DefaultScalaModule)

  def readEvents(filename:String) :  List[Event]  = {
    try {
      val jsonFile = Source.fromFile(filename)

      jsonFile
        .getLines()
        .map( line => mapper.readValue[Event](line))
        .toList

    } catch {
      case ex: FileNotFoundException =>
        println("File " + filename + " not found")
        sys.exit(1)

      case ex @ (
          _ : ValueInstantiationException |
          _ : JsonEOFException |
          _ : MismatchedInputException ) =>
        println("Unable to parse events from input file. " + ex.getMessage)
        sys.exit(1)
    }
  }

  def slidingWindowByTimestamp(windowSize: Long, events : List[Event]) : Seq[(LocalDateTime, List[Event])]  = {
    val orderedEvents = events.sortWith(_.timestamp < _.timestamp)
    val earliest = orderedEvents.head.timestampDateTime.truncatedTo(ChronoUnit.MINUTES)
    val latest = orderedEvents.takeRight(1).head.timestampDateTime.truncatedTo(ChronoUnit.MINUTES)

    (0.longValue() to earliest.until(latest, ChronoUnit.MINUTES) + 1)
      .map(i => earliest.plusMinutes(i))
      .map(datetime => {
        datetime -> events.filter(e => {
          val diff = e.timestampDateTime.until(datetime, ChronoUnit.MILLIS)
          diff > 0 && diff < windowSize * MILLIS_PER_MIN
        })
      })
  }

  def printAverageDeliveryTime(slidingWindow: Seq[(LocalDateTime, List[Event])]) : Unit = {

    case class output(
                       @JsonProperty("date") date: String,
                       @JsonProperty("average_delivery_time") avg_delivery_time: Double)

    val formatter = DateTimeFormatter.ofPattern(OUTPUTDATEFORMAT)

    slidingWindow
      .map(list => {
        val date = list._1.format(formatter)
        val avg = list._2.map(_.duration).sum/list._2.length.toDouble

        output(date, if(avg.isNaN) 0 else avg )
      })
      .foreach( value => println(mapper.writeValueAsString(value)))
  }

}
