package com.unbabel.event

import java.io.FileNotFoundException
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

import com.unbabel.config.Constants.OUTPUTDATEFORMAT
import com.unbabel.exception.InvalidEventException
import org.scalatest.FunSuite

/** Tests the method defined in the object  [[com.unbabel.event.EventHandler]]
  *
  * The following functions are tested: readEvents, slidingWindowByTimestamp and calculateAverageDeliveryTime
  */
class EventHandlerTestSuite extends FunSuite{

  private val event1 = Event("2018-12-26 18:11:08.509654","5aa5b2f39f7254a75aa5","en","fr","easyjet","translation_delivered",20,30)
  private val event2 = Event("2018-12-26 18:15:19.903159","5aa5b2f39f7254a75aa4","en","fr","easyjet", "translation_delivered",31, 30)
  private val event3 = Event("2018-12-26 18:23:19.903159","5aa5b2f39f7254a75bb33","en","fr","booking", "translation_delivered",54, 100)

  private val file_event_success_1 = "/events_success_1.json"
  private val file_event_success_2 = "/events_success_2.json"
  private val file_event_success_3 = "/events_success_3.json"
  private val file_event_failure_1 = "/events_failure_1.json"
  private val file_unexistent = "/my-unexistent-events-file.json"

  private val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
  private val outputformatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SS")
  private val outputStrLocalTime = LocalDateTime.parse("2018-12-26 18:11" , formatter )

  // Testing function EventHandler.readEvents(...)

  test("EventHandler reads valid event JSON files successfully") {
    val path = getClass.getResource(file_event_success_1).getPath
    val eventsParsed = EventHandler.readEvents(path)

    assert(eventsParsed.size == 3)
    assert(eventsParsed.head.equals(event1))
    assert(eventsParsed(1).equals(event2))
    assert(eventsParsed(2).equals(event3))
  }

  test("EventHandler returns empty list when JSON file is empty") {
    val path = getClass.getResource(file_event_success_2).getPath
    val eventsParsed = EventHandler.readEvents(path)
    assert(eventsParsed.isEmpty)
  }

  test("EventHandler fails reading file with invalid event") {
    assertThrows[InvalidEventException]{
      val path = getClass.getResource(file_event_failure_1).getPath
      EventHandler.readEvents(path)
    }
  }

  test("EventHandler fails finding unexistent event file") {
     assertThrows[FileNotFoundException](EventHandler.readEvents(file_unexistent))
  }


  // Testing function EventHandler.slidingWindowByTimestamp(...)

  test("EventHandler creates sliding window with positive window size") {
    val path = getClass.getResource(file_event_success_3).getPath
    val eventsParsed = EventHandler.readEvents(path)

    val res = Seq(
      (outputStrLocalTime, List()),
      (outputStrLocalTime.plusMinutes(1), List(event1)),
      (outputStrLocalTime.plusMinutes(2), List(event1)),
      (outputStrLocalTime.plusMinutes(3), List(event1)),
      (outputStrLocalTime.plusMinutes(4), List() ),
      (outputStrLocalTime.plusMinutes(5), List(event2)))

    val test = EventHandler.slidingWindowByTimestamp(3, eventsParsed)

    assert(test.equals(res))
  }

  test("EventHandler creates sliding window with window size 0 ") {
    val path = getClass.getResource(file_event_success_3).getPath
    val eventsParsed = EventHandler.readEvents(path)

    val res = Seq(
      (outputStrLocalTime, List()),
      (outputStrLocalTime.plusMinutes(1), List()),
      (outputStrLocalTime.plusMinutes(2), List()),
      (outputStrLocalTime.plusMinutes(3), List()),
      (outputStrLocalTime.plusMinutes(4), List()),
      (outputStrLocalTime.plusMinutes(5), List()))
    val test = EventHandler.slidingWindowByTimestamp(0, eventsParsed)

    assert(test.equals(res))
  }

  test("EventHandler creates empty sliding window with no events ") {
    val path = getClass.getResource(file_event_success_2).getPath
    val eventsParsed = EventHandler.readEvents(path)
    val test = EventHandler.slidingWindowByTimestamp(3, eventsParsed)

    assert(test.equals(Seq()))
  }



  // Testing function EventHandler.calculateAverageDeliveryTime(...)

  test("EventHandler generates aggregated average delivery time from non-empty sliding window") {

    val sw = Seq(
      (outputStrLocalTime, List()),
      (outputStrLocalTime.plusMinutes(1), List(event1)),
      (outputStrLocalTime.plusMinutes(2), List(event1)),
      (outputStrLocalTime.plusMinutes(3), List(event1)),
      (outputStrLocalTime.plusMinutes(4), List() ),
      (outputStrLocalTime.plusMinutes(5), List(event2)))

    val res = Seq(
      AvgDeliveryTime(outputStrLocalTime.format(outputformatter), 0),
      AvgDeliveryTime(outputStrLocalTime.plusMinutes(1).format(outputformatter), 20),
      AvgDeliveryTime(outputStrLocalTime.plusMinutes(2).format(outputformatter), 20),
      AvgDeliveryTime(outputStrLocalTime.plusMinutes(3).format(outputformatter), 20),
      AvgDeliveryTime(outputStrLocalTime.plusMinutes(4).format(outputformatter), 0),
      AvgDeliveryTime(outputStrLocalTime.plusMinutes(5).format(outputformatter), 31)
    )

    val test = EventHandler.calculateAverageDeliveryTime(sw)

    assert(test.equals(res))
  }

  test("EventHandler generates empty aggregated average delivery time with from empty sliding window") {

    val test = EventHandler.calculateAverageDeliveryTime(Seq())
    assert(test.equals(Seq()))
  }


}
