# Project Title

	Aggregator-cli: Agregate every minute event

# Getting Started

	- Requeriments

		- Sbt 1.2.8+
		- Scala 2.12
		- Java 8
			
	- Installation
		
		sbt clean compile test assembly
	
	- Running
	
		`cd target/scala-2.12/aggregator.jar`
		`java -jar aggregator.jar --input-file=<file> --window-size=<intervalTime>`
		