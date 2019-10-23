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

  // Requires that STRING fields are not null or empty
  require(timestamp != null && !timestamp.isEmpty, "The event field TIMESTAMP must not be null or empty")
  require(translation_id != null && !translation_id.isEmpty, "The event field TRANSLATION_ID must not be null or empty")
  require(lang_src != null && !lang_src.isEmpty, "The event field SOURCE_LANGUAGE must not be null or empty")
  require(lang_trg != null && !lang_trg.isEmpty, "The event field TARGET_LANGUAGE must not be null or empty")
  require(client != null && !client.isEmpty, "The event field CLIENT_NAME must not be null or empty")
  require(name != null && !name.isEmpty, "The event field EVENT_NAME must not be null or empty")

  // Requires that LONG fields are non-negative
  require(nr_words >= 0 && duration >= 0, "The event fields NR_WORDS and DURATION must be non-negative")

  // LocalDateTime based on timestamp
  private val formatter : DateTimeFormatter = DateTimeFormatter.ofPattern(INPUTDATEFORMAT)
  val timestampDateTime : LocalDateTime = LocalDateTime.parse(timestamp, formatter)

  def canEqual(that: Any) : Boolean = that.isInstanceOf[Event]

  override def equals(that: Any) : Boolean = {
    that match {
      case that: Event =>
        that.canEqual(this) &&
          this.timestamp.equals(timestamp) &&
          this.translation_id.equals(that.translation_id) &&
          this.lang_src.equals(that.lang_src) &&
          this.lang_trg.equals(that.lang_trg) &&
          this.client.equals(that.client) &&
          this.name.equals(that.name) &&
          this.duration == that.duration &&
          this.nr_words == that.nr_words

      case _ => false
    }
  }
}
