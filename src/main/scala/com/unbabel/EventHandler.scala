package com.unbabel

import java.io.FileNotFoundException

import com.unbabel.Constants._

import scala.io.Source

object EventHandler {

  type JSON = Map[String, String]

  def readEvents(filename:String) :  Array[Event]  = {
    try {

      println(s"Reading file " + filename)
      Source
        .fromFile(filename)
        .getLines()
        .toArray
        .map(line => parseEvent(Map(), prepareEventStr(line) ) )

    } catch {
      case ex: FileNotFoundException =>
        println("File " + filename + "not found")
        sys.exit(1) // TODO

      case ex: InvalidEventException =>
        println(ex.getMessage)
        sys.exit(1)

    }
  }

  private def prepareEventStr(str:String) : List [String] = {
    str
      .split(Array(COLON, COMMA))
      .toList
  }


  @throws(classOf[InvalidEventException])
  private def parseEvent(json:JSON, list:List[String]) : Event = {
    // TODO: ' ','\"'
    // TODO: Type validations, keynotfoundexception

    list match {

      case BRACES_CLS :: Nil => try {
        Event(
          json(TIMESTAMP),
          json(TRANSLATION_ID),
          json(LANG_SRC),
          json(LANG_TRG),
          json(CLIENT),
          json(NAME),
          json(NR_WORDS).toLong,
          json(DURATION).toLong
        )
      } catch {
        case ex: ClassCastException =>
          throw new InvalidEventException(ex.getMessage)
          //TODO: Key not found
      }

      case elem::Nil =>
        throw new InvalidEventException("Missing value for elem " + json + " on event " + list)

      case BRACES_OPN :: tail =>
        parseEvent(json, tail)

      case TIMESTAMP :: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(TIMESTAMP -> value.trim), tail)

      case TRANSLATION_ID :: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(TRANSLATION_ID -> value.trim), tail)

      case LANG_SRC :: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(LANG_SRC -> value.trim), tail)

      case LANG_TRG :: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(LANG_TRG -> value.trim), tail)

      case CLIENT :: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(CLIENT -> value.trim), tail)

      case NAME:: QT :: value :: QT :: tail =>
        parseEvent(json ++ Map(NAME -> value.trim), tail)

      case NR_WORDS :: value ::tail =>
        parseEvent(json ++ Map(NR_WORDS -> value.trim), tail)

      case DURATION :: value ::tail =>
        parseEvent(json ++ Map(DURATION -> value.trim), tail)
    }

  }

}
