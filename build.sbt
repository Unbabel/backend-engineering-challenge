name := "aggregator"

version := "0.1"

scalaVersion := "2.12.8"

lazy val versions = new {
  val jacksson = "2.9.5"
  val clist = "3.3.0"
  val scalaTest = "3.0.8"
  val mockito = "2.23.0"
}

libraryDependencies ++= Seq(
  "com.fasterxml.jackson.datatype" % "jackson-datatype-jsr310" % versions.jacksson,
  "com.fasterxml.jackson.core" % "jackson-databind" % versions.jacksson,
  "com.fasterxml.jackson.module" %% "jackson-module-scala" % versions.jacksson,
  "org.backuity.clist" %% "clist-core" % versions.clist,
  "org.backuity.clist" %% "clist-macros" % versions.clist,
  "org.scalatest" %% "scalatest" % versions.scalaTest % "test",
  "org.mockito" % "mockito-core" % versions.mockito % Test
)

assemblyJarName := "aggregator.jar"