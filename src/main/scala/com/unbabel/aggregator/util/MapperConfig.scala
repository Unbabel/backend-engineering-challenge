package com.unbabel.aggregator.util

import com.fasterxml.jackson.core.`type`.TypeReference
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule

class MapperConfig extends ObjectMapper {
  registerModule(DefaultScalaModule)
}

object MapperConfig {
  def mapper = new MapperConfig()

  def toJson(obj: Any) = mapper.writeValueAsString(obj)

  def fromJson[T](s: String): T = mapper.readValue(s, new TypeReference[T] {})
}
