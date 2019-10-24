package com.unbabel.aggregator.util

import org.scalatest.FunSuite

class MapperConfigTest extends FunSuite {
  val json = "{\"name\":\"Bruno\"}"
  val obj = Map("name" -> "Bruno")

  test("testToJson") {
    assertResult(json)(MapperConfig.toJson(obj))
  }

  test("testFromJson") {
    assertResult(obj)(MapperConfig.fromJson(json))
  }

}
