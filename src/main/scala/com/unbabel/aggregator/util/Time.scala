package com.unbabel.aggregator.util

import java.sql.Timestamp
import java.text.SimpleDateFormat
import java.time.{Instant, LocalDateTime}

import com.unbabel.aggregator.util.TimeConverters._

object Time {
  private val df = new SimpleDateFormat("yyyy-MM-dd HH:mm")

  def byMinute(date: String): Timestamp = df.parse(date).toInstant
}


object TimeConverters {
  implicit def localDateTime2timestamp(ldt: LocalDateTime): Timestamp = Timestamp.valueOf(ldt)

  implicit def instant2timestamp(i: Instant): Timestamp = Timestamp.from(i)

  implicit val ordered = new Ordering[Timestamp] {
    override def compare(x: Timestamp, y: Timestamp) = x compareTo y
  }

  implicit class LocalDate(time: Timestamp) {
    def minusMinutes(windowSize: Int): Timestamp = time.toLocalDateTime.minusMinutes(windowSize)
  }

}
