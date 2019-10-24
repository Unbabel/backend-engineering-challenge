# Backend Engineering Challenge

This project aims at creating a simple command line application that parses a stream of events and produces an aggregated output, which calculates a minute-by-minute moving average of the translation delivery time for the last X minutes.

## Getting Started

### Prerequisites ###
In order to build and run this project, please ensure you have the following tools installed on your machine:
+ Maven
+ Scala 2.11


### Usage

To run the program, execute the following command in the root of the project:

    ./unbabel_cli --input_file <path to file> --window_size <size>

As it can be seen above, the program receives the following parameters:
+ __--input_file__: Path to JSON events
+ __--window_size__: Size of the sliding window. Must be a non-negative long value.

### Build 

The project uses Maven for automating the building process, which includes dependency and test management. In order to build the project, please run the following command on the root directory:

    mvn clean package

When building this project, the following dependencies are automatically fetch from the [Central Maven Repository](https://mvnrepository.com/) :
+ jackson-module-scala_2.11
+ scalatest_2.11 


## Authors

+ Cláudia Henriques