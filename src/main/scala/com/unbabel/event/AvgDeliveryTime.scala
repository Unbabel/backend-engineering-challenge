package com.unbabel.event

import com.fasterxml.jackson.annotation.JsonProperty

case class AvgDeliveryTime(
                   @JsonProperty("date") date: String,
                   @JsonProperty("average_delivery_time") avg_delivery_time: Double)

