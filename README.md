# Backend Engineering Challenge


Welcome to our Engineering Challenge repository 🖖

If you found this repository it probably means that you are participating in our recruitment process. Thank you for your time and energy. If that's not the case please take a look at our [openings](https://unbabel.com/careers/) and apply!

Please fork this repo before you start working on the challenge, read it careful and take your time and think about the solution. Also, please fork this repository because we will evaluate the code on the fork.

This is an opportunity for us both to work together and get to know each other in a more technical way. If you have some doubt please open and issue and we'll reach out to help.

Good luck!

## Challenge Scenario

At Unbabel we deal with a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation. 

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### *translation_delivered*

Example:

```json
{
	"timestamp": "2018-12-26 18:12:19.903159",
	"translation_id": "5aa5b2f39f7254a75aa4",
	"source_language": "en",
	"target_language": "fr",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"duration": 20,
	"nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

	unbabel_cli --input_file events.json --window_size 10
	
The input file format would be something like:

	{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
	{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
	{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}


The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

#### Notes

Before jumping right into implementation we advise you to think about the solution first. We will evaluate, not only if your solution works but also the following aspects:

+ Simple and easy to read code. Remember that [simple is not easy](https://www.infoq.com/presentations/Simple-Made-Easy)
+ Include a README.md that briefly describes how to build and run your code
+ Be consistent in your code. 

Feel free to include, in your solution, some your considerations while doing this challenge. We want you to solve this challenge in the language you feel most confortable with. Our machines run Python, Ruby, Scala, Java, Clojure, Elixir and Nodejs. If you are thinking of using any other programming language please reach out to us first 🙏.

Also if you have any problem please **open an issue**. 

Good luck and may the force be with you

#### Extra points

If you feeling creative feel free to consider any additional cases you might find interesting. Remember this is a bonus, focus on delivering the solution first.

## Submitted solution (Go)

This is a very simple implementation of the task in question.
The code submitted is in Go version 1.17

The folder contains:
- main.go containing the source code
- events.json containing the input example above

To run the code:
- go to the same directory (unbabel_cli) as the main.go and events.json:
`cd unbabel_cli`
- to run the code:
`go run main.go`
This would work without command line arguments as they are set by default to the wanted values (input_file="events.json" and window=10)
You can also build the code and run the executable:
`go build`
`./unbabel_cli -input_file events.json -window_size 10`
or
`go install`
`unbabel_cli -input_file events.json -window_size 10`
which will add the exectuable to the bin in your GOPATH

To understand more the command line arguments expected, what are they and their default values, run:
`go run main.go -h` or `./unbabel_cli -h` or `unbabel_cli -h`
This will output the following:
```
Usage of unbabel_cli:
  -client_name string
        client name for which the events should be considered
  -event_name string
        event name for which the events should be considered (default "translation_delivered")
  -input_file string
        path to the input file containing the events (default "events.json")
  -input_time_layout string
        format of the input timestamp to read from the input json file (default "2006-01-02 15:04:05.999999")
  -output_file string
        path to the output file where the events delivery time moving average is stored (default "output.json")
  -output_time_layout string
        format of the output timestamp to write to the output json file (default "2006-01-02 15:04:05")
  -source_language string
        source language for which the events should be considered
  -target_language string
        target language for which the events should be considered
  -window_size int
        number of minutes for which to calculate the moving average (default 10)
```
I added some command line arguments to allow calculating the moving avergae of delivery duration while selecting the client name, source langauge, target language and event name.
By default those are not taken into consideration and therefore all the events are considered.
Also, it allows picking the format of time for input and output, as well as the path to the output file. These are set by default to suit the example.

Once the code runs correctly, the output file (output.json) is created and contains the expected output.

If there any questions or improvements needed, please do not hesitate to reach out. Cheers!

