package com.unbabel.aggregator.util

import java.sql.Timestamp

import com.fasterxml.jackson.annotation.JsonProperty
import com.unbabel.aggregator.util.TimeConverters._

object Metric {
  def max[T](values: Seq[T], evt: T => Timestamp): Timestamp = values.map(evt(_)).max

  def average(values: Seq[Double]): Double = values.sum / values.size
}


case class Output(
                   @JsonProperty("date") date: String,
                   @JsonProperty("average_delivery_time") averageDeliveryTime: Double
                 )
