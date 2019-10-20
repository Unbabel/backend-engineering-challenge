package com.unbabel

import com.unbabel.config.Constants._
import com.unbabel.event.EventHandler

import scala.util.Try

object UnbabelCli  {

  case class Arguments(inputFile : String, windowSize : Long)

  def main(args: Array[String]): Unit = {
    println("Welcome to Unbabel Cli")

    val arguments = try parseArguments(Map(), args.toList) catch {
      case ex: IllegalArgumentException =>
        printUsage()
        println(ex.getMessage)
        sys.exit(1)
    }

    val events = EventHandler.readEvents(arguments.inputFile)
    val slidingWindow = EventHandler.slidingWindowByTimestamp(arguments.windowSize, events)
    EventHandler.printAverageDeliveryTime(slidingWindow)

    println("Exiting Unbabel Cli")
    sys.exit(0)
  }

  @throws(classOf[IllegalArgumentException])
  private def parseArguments(map : Map[String, Any], list: List[String]) : Arguments = {

    list match {
      case Nil => try
        Arguments(map(ARG_INPUTFILE).asInstanceOf[String], map(ARG_WINDOWSIZE).asInstanceOf[Long])
        catch {
          case ex: NoSuchElementException =>
            throw new IllegalArgumentException("Missing argument. " + ex.getMessage)
        }

      case option :: Nil =>
        throw new IllegalArgumentException("Missing value for option " + option)

      case ARG_INPUTFILE :: value :: tail =>
        parseArguments(map ++ Map(ARG_INPUTFILE -> value), tail)

      case ARG_WINDOWSIZE :: value :: tail =>
        if(Try(value.toLong).isSuccess)
          parseArguments(map ++ Map(ARG_WINDOWSIZE -> value.toLong), tail)
        else
          throw new IllegalArgumentException("The argument " + ARG_WINDOWSIZE + " should be a Long value")

      case option :: tail =>
        throw new IllegalArgumentException("Unknown option " + option)
    }
  }

  private def printUsage() : Unit = {
    val usage = "Usage: unbabel_cli --input_file <path_to_file> --window_size <size>"
    println(usage)
  }

}
