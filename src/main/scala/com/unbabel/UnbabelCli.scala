package com.unbabel

import com.unbabel.Constants._

import scala.util.Try

object UnbabelCli  {

  type ArgumentsMap = Map[Symbol, Any]

  def main(args: Array[String]): Unit = {
    println("Welcome to Unbabel Cli")

    var inputFile: String = ""
    var windowSize : Long = 0

    try {
      val arguments = parseArguments(Map(), args.toList)

      if(arguments.size < 2) {
        printUsage()
        sys.exit(1)
      }

      inputFile = arguments(Symbol(ARG_INPUTFILE)).asInstanceOf[String]
      windowSize = arguments(Symbol(ARG_WINDOWSIZE)).asInstanceOf[Long]


    } catch {
      case ex: IllegalArgumentException =>
        printUsage()
        println(ex.getMessage)
        sys.exit(1)
    }

    val events = EventHandler.readEvents(inputFile)
    EventHandler.slidingByTimestamp(windowSize, events)

    println("Exiting Unbabel Cli")
    sys.exit(0)
  }

  @throws(classOf[IllegalArgumentException])
  private def parseArguments(map : ArgumentsMap, list: List[String]) : ArgumentsMap = {

    list match {
      case Nil => map

      case option :: Nil =>
        throw new IllegalArgumentException("Missing value for option " + option)

      case ARG_INPUTFILE :: value :: tail =>
        parseArguments(map ++ Map(Symbol(ARG_INPUTFILE) -> value), tail)

      case ARG_WINDOWSIZE :: value :: tail =>
        if(Try(value.toLong).isSuccess)
          parseArguments(map ++ Map(Symbol(ARG_WINDOWSIZE) -> value.toLong), tail)
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
