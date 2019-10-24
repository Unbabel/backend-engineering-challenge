package com.unbabel.aggregator

import java.sql.Timestamp

import com.unbabel.aggregator.event.Event
import com.unbabel.aggregator.util.Metric
import org.scalatest.FunSuite

class MetricTest extends FunSuite {
val events = Seq(Event("2018-12-26 18:23:19.903159","5aa5b2f39f7254a75bb33","en","fr","booking","translation_delivered",54,100),
  Event("2018-12-26 18:24:19.903159","5aa5b2f39f7254a75bb33","en","fr","booking","translation_delivered",60,100))

  test("testMax") {
    assertResult(Timestamp.valueOf("2018-12-26 18:24:00"))(Metric.max[Event](events, _.getTime))
  }

  test("testAverage") {
    val values = Seq(32.5D,25D)
    assertResult(28.75D)(Metric.average(values))
  }

}
