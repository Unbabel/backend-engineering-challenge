package com.unbabel.event

import org.scalatest.FunSuite

/** Tests event creation
  *
  * This suite tests the class [[com.unbabel.event.Event]] by creating both valid and invalid events.
  */
class EventTestSuite extends FunSuite {

  val timestamp = "2018-12-26 18:11:08.509654"
  val translation_id = "5aa5b2f39f7254a75aa5"
  val lang_src = "en"
  val lang_trg = "fr"
  val client = "easyjet"
  val name = "translation_delivered"
  val nr_words = 30
  val duration = 20

  test("Testing event creation with null STRING paramenters") {

    assertThrows[IllegalArgumentException] {
      Event(null, translation_id, lang_src, lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, null, lang_src, lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, null, lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, null, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, null, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, client, null, duration, nr_words)
    }
  }

  test("Testing event creation with empty STRING paramenters") {

    assertThrows[IllegalArgumentException] {
      Event(new String(), translation_id, lang_src, lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, new String(), lang_src, lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, new String(), lang_trg, client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, new String(), client, name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, new String(), name, duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, client, new String(), duration, nr_words)
    }
  }

  test("Testing event creation with negative LONG parameters") {
    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, client, name, -duration, nr_words)
    }

    assertThrows[IllegalArgumentException] {
      Event(timestamp, translation_id, lang_src, lang_trg, client, name, duration, -nr_words)
    }
  }

  test("Testing event creation under with with non-empty nor null STRING parameters and non-negative LONG parameters ") {
    val event = Event(timestamp, translation_id, lang_src, lang_trg, client, name, duration, nr_words)

    assert(event.timestamp == timestamp)
    assert(event.translation_id == translation_id)
    assert(event.lang_src == lang_src)
    assert(event.lang_trg == lang_trg)
    assert(event.client == client)
    assert(event.name == name)
    assert(event.duration == duration)
    assert(event.nr_words == nr_words)

  }

}