package com.unbabel

import java.io.FileNotFoundException
import java.time.temporal.ChronoUnit

import scala.io.Source
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}
import com.unbabel.Constants._

object EventHandler {

  def readEvents(filename:String) :  List[Event]  = {
    try {
      // TODO jackson exceptions
      val jsonFile = Source.fromFile(filename)
      val mapper = new ObjectMapper() with ScalaObjectMapper
      mapper.registerModule(DefaultScalaModule)

      jsonFile
        .getLines()
        .map( line => mapper.readValue[Event](line))
        .toList

    } catch {
      case ex: FileNotFoundException =>
        println("File " + filename + " not found")
        sys.exit(1) // TODO

      case ex: InvalidEventException =>
        println(ex.getMessage)
        sys.exit(1)
    }
  }

  def slidingByTimestamp(windowSize: Long, events : List[Event]) : Unit = {

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
      }).foreach(println)

  }



}
