package com.unbabel.aggregator

import java.io.File

import com.unbabel.aggregator.event.{EventFile, EventService}
import com.unbabel.aggregator.util.MapperConfig._
import org.backuity.clist._


object CliAggregator extends CliMain[Unit] {
  var inputFile = opt[Boolean](description = " <file>")
  var windowSize = opt[Boolean](description = " <window>")

  var file = arg[File](name = "input-file")
  var window = arg[Int](name = "window-size")

  override def run: Unit = {
    val aggregator = new AverageDeliver(new EventService(EventFile(file)), new JsonPrinter)
    aggregator.run(window)
    aggregator.print()
  }
}