package com.unbabel.aggregator

import java.sql.Timestamp

import com.unbabel.aggregator.event.{Event, EventService}
import com.unbabel.aggregator.util.Output
import org.mockito.Mockito
import org.scalatest.FunSuite
import org.scalatestplus.mockito.MockitoSugar

class AverageDeliverTest extends FunSuite with MockitoSugar {
  val eventsByTime = Map(
    Timestamp.valueOf("2018-12-26 18:24:00.0") -> Seq(Event("2018-12-26 18:24:19.903159", "5aa5b2f39f7254a75bb33", "en", "fr", "booking", "translation_delivered", 60, 100),
      Event("2018-12-26 18:24:19.903159", "5aa5b2f39f7254a75bb33", "en", "fr", "booking", "translation_delivered", 120, 100)))

  test("testRun") {
    val eventService = mock[EventService]
    Mockito.when(eventService.eventByTime(5)).thenReturn(eventsByTime)
    val averageDeliver = new AverageDeliver(eventService, new JsonPrinter)
    averageDeliver.run(5)

    assertResult(Seq(Output("2018-12-26 18:24:00.0", 90.0)))(averageDeliver.eventsAggregator)
  }
}
