package com.unbabel

import java.io.FileNotFoundException

import com.unbabel.config.Constants._
import com.unbabel.event.EventHandler
import com.unbabel.exception.InvalidEventException

import scala.util.Try


object UnbabelCli  {

  /** Holds the arguments provided by the user
    *
    * @param inputFile Input File with JSON data
    * @param windowSize Size of the sliding window
    */
  case class Arguments(inputFile : String, windowSize : Long)

  /** Parses a stream of events and produces an aggregated output.
    *
    * @param args Input arguments
    */
  def main(args: Array[String]): Unit = {

    // Parse input arguments. Program stops in case of IllegalArgumentException.
    val arguments = try parseArguments(Map(), args.toList) catch {
      case ex: IllegalArgumentException =>
        printUsage()
        println(ex.getMessage)
        sys.exit(1)
    }

    // Reads events. Program stops in case of errors.
    val events = try EventHandler.readEvents(arguments.inputFile) catch {
      case ex @ ( _: FileNotFoundException | _ : InvalidEventException ) =>
        println(ex.getMessage)
        sys.exit(1)

    }

    // Creates the sliding windows and prints the result of the average delivery time
    val slidingWindow = EventHandler.slidingWindowByTimestamp(arguments.windowSize, events)
    val avgDeliveryTime = EventHandler.calculateAverageDeliveryTime(slidingWindow)
    EventHandler.printAverageDeliveryTime(avgDeliveryTime)

    sys.exit(0)
  }


  /** Returns [[com.unbabel.UnbabelCli.Arguments]] with the input arguments. This function is called recursively.
    *
    * @param argsParsed Map of user input arguments already parsed. In the first iteration, an empty map is excepted.
    * @param listArgs List of arguments yet to be parsed.
    * @throws java.lang.IllegalArgumentException Thrown when the arguments passed to the program are not the ones expected
    * @return Input arguments parsed.
    */
  @throws(classOf[IllegalArgumentException])
  private def parseArguments(argsParsed : Map[String, Any], listArgs: List[String]) : Arguments = {

    listArgs match {

      // Returns the object Arguments if there aren't any more user inputs to parse.
      // Throws an IllegalArgumentException in case a required argument is not provided by the user.
      case Nil => try
        Arguments(argsParsed(ARG_INPUTFILE).asInstanceOf[String], argsParsed(ARG_WINDOWSIZE).asInstanceOf[Long])
        catch {
          case ex: NoSuchElementException =>
            throw new IllegalArgumentException("Missing argument. " + ex.getMessage)
        }

      // Throws an IllegalArgumentException if an argument is provided without value.
      case option :: Nil =>
        throw new IllegalArgumentException("Missing value for argument " + option)

      // Recursively calls this method in case a known option is provided as expected.
      // Throws an IllegalArgumentException in case the value provided isn't castable to the expected type.
      case ARG_INPUTFILE :: value :: tail =>
        parseArguments(argsParsed ++ Map(ARG_INPUTFILE -> value), tail)

      case ARG_WINDOWSIZE :: value :: tail =>
        if(Try(value.toLong).isSuccess && value.toLong >= 0 )
          parseArguments(argsParsed ++ Map(ARG_WINDOWSIZE -> value.toLong), tail)
        else
          throw new IllegalArgumentException("The argument " + ARG_WINDOWSIZE + " receives a non-negative number")

        // Throws an IllegalArgumentException if an unknown option is provided by the user
      case option :: tail =>
        throw new IllegalArgumentException("Unknown argument " + option)
    }
  }

  /** Prints the usage of the current executable */
  private def printUsage() : Unit = {
    val usage = "Usage: unbabel_cli --input_file <path_to_file> --window_size <size>"
    println(usage)
  }
}
