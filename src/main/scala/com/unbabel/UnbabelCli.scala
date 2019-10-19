package com.unbabel

import com.unbabel.Constants.arg_inputfile

import scala.io.Source
import scala.util.Try

object UnbabelCli  {

  type ArgumentsMap = Map[Symbol, Any]

  def main(args: Array[String]): Unit = {
    println("Welcome to Unbabel Cli")

    try {
      val arguments = parseArguments(Map(), args.toList)

      if(arguments.size < 2) {
        printUsage()
        sys.exit(1)
      }

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
        val sym_inputfile = Symbol(arg_inputfile)
        parseArguments(map ++ Map(sym_inputfile -> value), tail)

      case Constants.arg_windowsize :: value :: tail =>
        val sym_windowsize = Symbol(arg_inputfile)
        if(Try(value.toLong).isSuccess)
          parseArguments(map ++ Map(sym_windowsize -> value.toLong), tail)
        else
          throw new IllegalArgumentException("The argument " + Constants.arg_windowsize + " should be a Long value")

      case option :: tail =>
        throw new IllegalArgumentException("Unknown option " + option)
    }
  }


  def printUsage() : Unit = {
    val usage = "Usage: unbabel_cli --input_file <path_to_file> --window_size <size>"
    println(usage)
  }

}
