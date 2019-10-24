package com.unbabel.aggregator

import com.unbabel.aggregator.util.{MapperConfig, Output}

trait Printer[T] {
  def print(obj: Seq[T]): Unit = obj.foreach(print)

  def print(obj: T): Unit
}


class JsonPrinter extends Printer[Output] {
  override def print(obj: Output): Unit = println(MapperConfig.toJson(obj))
}