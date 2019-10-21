package com.unbabel

import com.unbabel.config.Constants._
import com.unbabel.event.EventHandler
import scala.util.Try

/** Unbabel Client shell */
object UnbabelCli  {

  /** Holds the arguments provided by the user
    * @param inputFile Input File with JSON data
    * @param windowSize Size of the sliding window
    */
  case class Arguments(inputFile : String, windowSize : Long)

  /** Parses a stream of events and produces an aggregated output.
    * @param args Input arguments
    */
  def main(args: Array[String]): Unit = {
    println("Welcome to Unbabel Cli")

    // Parse input arguments. Stop the program in case of IllegalArgumentException.
    val arguments = try parseArguments(Map(), args.toList) catch {
      case ex: IllegalArgumentException =>
        printUsage()
        println(ex.getMessage)
        sys.exit(1)
    }

    // Reads events, create a sliding window and print the results to the user input
    val events = EventHandler.readEvents(arguments.inputFile)
    val slidingWindow = EventHandler.slidingWindowByTimestamp(arguments.windowSize, events)
    EventHandler.printAverageDeliveryTime(slidingWindow)

    // Exit
    println("Exiting Unbabel Cli")
    sys.exit(0)
  }

  /** Returns [[com.unbabel.UnbabelCli.Arguments]] with the input arguments. This function is called recursively. On each iteration, the result is added to the map and list of
    * @param map Map of user input arguments already parsed. In the first iteration, an empty map is excepted.
    * @param list List of arguments yet to be parsed.
    * @throws java.lang.IllegalArgumentException
    * @return Input arguments parsed.
    */
  @throws(classOf[IllegalArgumentException])
  private def parseArguments(map : Map[String, Any], list: List[String]) : Arguments = {

    list match {

        // Returns the object Arguments if there aren't any more user inputs to parse. Throws an IllegalArgumentException in case a required argument is not provided by the user.
      case Nil => try
        Arguments(map(ARG_INPUTFILE).asInstanceOf[String], map(ARG_WINDOWSIZE).asInstanceOf[Long])
        catch {
          case ex: NoSuchElementException =>
            throw new IllegalArgumentException("Missing argument. " + ex.getMessage)
        }

       // Throws an IllegalArgumentException if an argument is provided without value.
      case option :: Nil =>
        throw new IllegalArgumentException("Missing value for option " + option)

        // Recursively calls this method in case a known option is provided as expected. Throws an IllegalArgumentException in case the value provided isn't castable to the expected type.
      case ARG_INPUTFILE :: value :: tail =>
        parseArguments(map ++ Map(ARG_INPUTFILE -> value), tail)

      case ARG_WINDOWSIZE :: value :: tail =>
        if(Try(value.toLong).isSuccess)
          parseArguments(map ++ Map(ARG_WINDOWSIZE -> value.toLong), tail)
        else
          throw new IllegalArgumentException("The argument " + ARG_WINDOWSIZE + " should be a Long value")

        // Throws an IllegalArgumentException if an unknown option is provided by the user
      case option :: tail =>
        throw new IllegalArgumentException("Unknown option " + option)
    }
  }

  /** Prints the usage of the current executable */
  private def printUsage() : Unit = {
    val usage = "Usage: unbabel_cli --input_file <path_to_file> --window_size <size>"
    println(usage)
  }

}
