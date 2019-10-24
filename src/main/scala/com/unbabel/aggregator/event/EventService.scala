package com.unbabel.aggregator.event

import java.sql.Timestamp

import com.unbabel.aggregator.util.Metric._
import com.unbabel.aggregator.util.MapperConfig
import com.unbabel.aggregator.util.TimeConverters._

class EventService(
                    eventFile: EventFile
                  ) {

  private def events = eventFile.getContent.map(r => MapperConfig.mapper.readValue(r, classOf[Event]))

  def isValid(latest: Timestamp, earliest: Timestamp): Boolean = latest.after(earliest)

  def eventByTime(windowSize: Int): Map[Timestamp, Seq[Event]] =
    events
      .filter(e => isValid(e.getTime, max[Event](events, _.getTime).minusMinutes(windowSize)))
      .groupBy(_.getTime)
}

