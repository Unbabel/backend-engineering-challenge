package com.unbabel.aggregator.event

import java.io.File

import scala.io.Source

case class EventFile(file: File) {

  def getContent: Seq[String] =
    Option(Source.fromFile(file))
      .map(_.getLines())
      .map(_.toSeq)
      .getOrElse(throw new IllegalArgumentException("Error while reading file!"))
}
