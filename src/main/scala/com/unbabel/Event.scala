package com.unbabel

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

import com.fasterxml.jackson.annotation.JsonProperty
import com.unbabel.Constants._

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

  private val formatter = DateTimeFormatter.ofPattern(INPUTDATEFORMAT)
  val timestampDateTime = LocalDateTime.parse(timestamp, formatter)

}
