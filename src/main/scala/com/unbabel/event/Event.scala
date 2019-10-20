package com.unbabel.event

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

import com.fasterxml.jackson.annotation.JsonProperty
import com.unbabel.config.Constants._

/** An event resulting from a translation
  *
  * @param timestamp Timestamp of the translation
  * @param translation_id Id of the translation
  * @param lang_src Source language of the translation
  * @param lang_trg Target language of thre translation
  * @param client Name of the client
  * @param name Name of the event
  * @param duration Duration of the translation
  * @param nr_words Number of words translated
  */
case class Event(
                  @JsonProperty("timestamp") timestamp: String ,
                  @JsonProperty("translation_id") translation_id: String,
                  @JsonProperty("source_language") lang_src: String,
                  @JsonProperty("target_language") lang_trg: String,
                  @JsonProperty("client_name") client: String,
                  @JsonProperty("event_name") name: String,
                  @JsonProperty("duration") duration: Long,
                  @JsonProperty("nr_words") nr_words: Long
                ) {

  val formatter = DateTimeFormatter.ofPattern(INPUTDATEFORMAT)
  val timestampDateTime = LocalDateTime.parse(timestamp, formatter)

}
