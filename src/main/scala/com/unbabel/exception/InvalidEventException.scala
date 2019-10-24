package com.unbabel.exception

/** Exception thrown in case a given [[com.unbabel.event.Event]] is not valid
  *
  * @param message Message to be sent to the user that summarizes what caused the problem
  */
class InvalidEventException(message: String) extends Exception(message) {

  def this(message: String, cause: Throwable) {
    this(message)
    initCause(cause)
  }

  def this(cause: Throwable) {
    this(Option(cause).map(_.toString).orNull, cause)
  }

  def this() {
    this(null: String)
  }
}
