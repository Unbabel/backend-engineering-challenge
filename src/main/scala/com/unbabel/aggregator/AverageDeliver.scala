package com.unbabel.aggregator

import com.unbabel.aggregator.util.Metric._
import com.unbabel.aggregator.event.EventService
import com.unbabel.aggregator.util.Output
import com.unbabel.aggregator.util.TimeConverters._

class AverageDeliver(
                      eventService: EventService,
                      printer: Printer[Output]
                    ) extends Aggregator[Int, Seq[Output]] {
  var eventsAggregator: Seq[Output] = _

  def run(input: Int): Unit = { // input = window size
    eventsAggregator = eventService.eventByTime(input)
      .map(e => (e._1, average(e._2.map(_.duration.toDouble)))) // calculate avg time by slots of minutes
      .toSeq
      .sortBy(_._1)
      .map(agg => Output(agg._1.toString, agg._2))
  }

  def print(): Unit = printer.print(eventsAggregator)
}

trait Aggregator[I, O] {
  var eventsAggregator: O

  def run(input: I): Unit
}