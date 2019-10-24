package com.unbabel.aggregator.util

import java.sql.Timestamp

import org.scalatest.FunSuite

class TimeTest extends FunSuite {

  test("testByMinute") {
    assertResult(Timestamp.valueOf("2019-10-24 10:12:00"))(Time.byMinute("2019-10-24 10:12:11.987654"))
  }

}
