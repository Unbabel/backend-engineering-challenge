package com.unbabel.aggregator.event

import java.sql.Timestamp

import org.mockito.Mockito
import org.scalatest.{BeforeAndAfter, FunSuite}
import org.scalatestplus.mockito.MockitoSugar

class EventServiceTest extends FunSuite with BeforeAndAfter with MockitoSugar {
  var eventService: EventService = _
  val eventFile: EventFile = mock[EventFile]
  val content = Seq("{\"timestamp\": \"2018-12-26 18:23:19.903159\",\"translation_id\": \"5aa5b2f39f7254a75bb33\",\"source_language\": \"en\",\"target_language\": \"fr\",\"client_name\": \"booking\",\"event_name\": \"translation_delivered\",\"nr_words\": 100, \"duration\": 54}",
    "{\"timestamp\": \"2018-12-26 18:23:19.903159\",\"translation_id\": \"5aa5b2f39f7254a75bb33\",\"source_language\": \"en\",\"target_language\": \"fr\",\"client_name\": \"booking\",\"event_name\": \"translation_delivered\",\"nr_words\": 100, \"duration\": 30}",
    "{\"timestamp\": \"2018-12-26 18:24:19.903159\",\"translation_id\": \"5aa5b2f39f7254a75bb33\",\"source_language\": \"en\",\"target_language\": \"fr\",\"client_name\": \"booking\",\"event_name\": \"translation_delivered\",\"nr_words\": 100, \"duration\": 60}",
    "{\"timestamp\": \"2018-12-26 18:24:19.903159\",\"translation_id\": \"5aa5b2f39f7254a75bb33\",\"source_language\": \"en\",\"target_language\": \"fr\",\"client_name\": \"booking\",\"event_name\": \"translation_delivered\",\"nr_words\": 100, \"duration\": 120}")

  before {
    Mockito.when(eventFile.getContent).thenReturn(content)
    eventService = new EventService(eventFile)
  }

  test("testEventByTime") {
    val expected = Map(
      Timestamp.valueOf("2018-12-26 18:24:00.0") -> Seq(Event("2018-12-26 18:24:19.903159", "5aa5b2f39f7254a75bb33", "en", "fr", "booking", "translation_delivered", 60, 100),
        Event("2018-12-26 18:24:19.903159", "5aa5b2f39f7254a75bb33", "en", "fr", "booking", "translation_delivered", 120, 100))
    )

    assertResult(expected)(eventService.eventByTime(1))
  }

  test("testIsValid") {
    val eventService = new EventService(mock[EventFile])
    val time1 = Timestamp.valueOf("2019-10-24 01:00:00")
    val time2 = Timestamp.valueOf("2019-10-24 00:00:00")

    assert(eventService.isValid(time1, time2))
  }
}
