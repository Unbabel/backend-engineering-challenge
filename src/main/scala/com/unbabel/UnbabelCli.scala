package com.unbabel

import scala.io.Source
import scala.util.Try

object UnbabelCli  {

  type ArgumentsMap = Map[Symbol, Any]

  def main(args: Array[String]): Unit = {
    println("Welcome to Unbabel Cli")

    if (args.length == 0) printUsage()

    try {
      val arguments = parseArguments(Map(), args.toList)


    } catch {
      case ex: IllegalArgumentException =>
        printUsage()
        println(ex.getMessage)
        sys.exit(1)
    }

    println("Exiting Unbabel Cli")
    sys.exit(0)
  }

  @throws(classOf[IllegalArgumentException])
  def parseArguments(map : ArgumentsMap, list: List[String]) : ArgumentsMap = {

    list match {
      case Nil => map

      case option :: Nil =>
        throw new IllegalArgumentException("Missing value for option " + option)

      case Constants.arg_inputfile :: value :: tail =>
        parseArguments(map ++ Map(Constants.sym_inputfile -> value), tail)


      case Constants.arg_windowsize :: value :: tail =>
        if(Try(value.toLong).isFailure)
          throw new IllegalArgumentException("The argument " + Constants.arg_windowsize + " should be a Long value")
        else
          parseArguments(map ++ Map(Constants.sym_windowsize -> value.toLong), tail)

      case option :: tail =>
        throw new IllegalArgumentException("Unknown option " + option)
    }
  }


  def printUsage() : Unit = {
    val usage = "Usage: unbabel_cli --input_file <path_to_file> --window_size <size>"
    println(usage)
  }

}
