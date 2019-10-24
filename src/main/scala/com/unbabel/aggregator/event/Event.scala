package com.unbabel.aggregator.event

import java.sql.Timestamp

import com.fasterxml.jackson.annotation.JsonProperty
import com.unbabel.aggregator.util.Time

case class Event(
                  @JsonProperty("timestamp") timestamp: String,
                  @JsonProperty("translation_id") translationId: String,
                  @JsonProperty("source_language") sourceLanguage: String,
                  @JsonProperty("target_language") targetLanguage: String,
                  @JsonProperty("client_name") clientName: String,
                  @JsonProperty("event_name") eventName: String,
                  @JsonProperty("duration") duration: Int,
                  @JsonProperty("nr_words") nrWords: Int
                ) {

  def getTime: Timestamp = Time.byMinute(timestamp)
}
