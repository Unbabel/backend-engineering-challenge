// Read an a stream of events from a json input file
// and a window representing a number of minutes
// for which we calculate the moving average of delivery
// durations. Write the output in the specified format
// in a json file.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"time"
)

// Event struct which contains the expected
// structure of an event read from the input file
type Event struct {
	Timestamp     string `json:"timestamp"`
	TranslationId string `json:"translation_id"`
	SourceLang    string `json:"source_language"`
	TargetLang    string `json:"target_language"`
	CliName       string `json:"client_name"`
	EventName     string `json:"event_name"`
	Duration      int    `json:"duration"`
	NumWords      int    `json:"nr_words"`
}

// AvgDeliveryTimeOutput struct which contains the expected
// structure to be written as output for the average delivery times
type AvgDeliveryTimeOutput struct {
	Date                string  `json:"date"`
	AverageDeliveryTime float32 `json:"average_delivery_time"`
}

func main() {

	// set the expected flags for the input file path
	// the window and the output file path
	inputFile := flag.String("input_file", "events.json", "path to the input file containing the events")
	window := flag.Int("window_size", 10, "number of minutes for which to calculate the moving average")
	eventName := flag.String("event_name", "translation_delivered", "event name for which the events should be considered")
	clientName := flag.String("client_name", "", "client name for which the events should be considered")
	sourceLang := flag.String("source_language", "", "source language for which the events should be considered")
	targetLang := flag.String("target_language", "", "target language for which the events should be considered")
	inputTimeLayout := flag.String("input_time_layout", "2006-01-02 15:04:05.999999", "format of the input timestamp to read from the input json file")
	outputTimeLayout := flag.String("output_time_layout", "2006-01-02 15:04:05", "format of the output timestamp to write to the output json file")
	outputFile := flag.String("output_file", "output.json", "path to the output file where the events delivery time moving average is stored")

	flag.Parse()

	// Open the json file
	jsonFile, err := os.Open(*inputFile)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	// read our opened jsonFile as a byte array.
	byteValue, _ := ioutil.ReadAll(jsonFile)

	// we declare our Event array
	var events []Event

	// we unmarshal our byteArray which contains our
	// json file's content into 'events' which we defined above
	// panic if an error occurs
	err = json.Unmarshal(byteValue, &events)
	if err != nil {
		panic(err)
	}

	// we set out zero time and parse the zero date
	// that will allow us later to calculate durations
	// panic if parsing returns an error
	zeroTime := "2000-01-01 00:00:00.000000"
	zeroDate, err := time.Parse(*inputTimeLayout, zeroTime)
	if err != nil {
		panic(err)
	}

	selectedEvents := selectEvents(events, *clientName, *sourceLang, *targetLang, *eventName)

	delivPerMinMap, minDuration, maxDuration := populateDelivMap(selectedEvents, *window, zeroDate, *inputTimeLayout)

	outputData := outputMovingAvg(delivPerMinMap, minDuration, maxDuration, zeroDate, *outputTimeLayout)

	// Marshall the returned output data
	file, err := json.MarshalIndent(outputData, "", " ")
	if err != nil {
		panic(err)
	}

	// write to the given output (default output.json) json file
	err = ioutil.WriteFile(*outputFile, file, 0644)
	if err != nil {
		panic(err)
	}
}

// calculate the moving average by summing the non-zero
// values previously associated with each event based on the window
// and return the moving average of each given slice of values
func calcMovingAvg(values []int) float32 {
	sum := 0
	count := 0
	for i := 0; i < len(values); i++ {
		if values[i] != 0 {
			sum += values[i]
			count += 1
		}
	}
	if sum == 0 {
		return 0.0
	} else {
		return float32(sum) / float32(count)
	}
}

func outputMovingAvg(delivPerMinMap map[int][]int, minEventTimeSinceZero int, maxEventTimeSinceZero int, zeroDate time.Time, outputTimeLayout string) []AvgDeliveryTimeOutput {
	// initialize the output slice that will hold
	// the data to be written to the output file
	var outputData []AvgDeliveryTimeOutput
	// loop since the time elapsed associated with the first (lowest timestamp) event
	// to the event associated with the last (highest timestamp) expected event
	for i := minEventTimeSinceZero; i <= maxEventTimeSinceZero; i++ {
		// compute moving average of the durations associated with the event
		movingAvg := calcMovingAvg(delivPerMinMap[i])
		// compute the timestamp based on the elapsed time of the event since zero
		// with the expected format output
		outputTime := zeroDate.Add(time.Minute * time.Duration(i)).Format(outputTimeLayout)
		// append output event to the output slice
		outputData = append(outputData, AvgDeliveryTimeOutput{Date: outputTime, AverageDeliveryTime: movingAvg})
	}
	return outputData
}

func populateDelivMap(selectedEvents []Event, window int, zeroDate time.Time, inputTimeLayout string) (map[int][]int, int, int) {

	// initialize a map from int to a slice onf ints
	// it will map a duration of the event since zeroTime calculated in minutes
	// to a slice of durations based on the window
	delivPerMinMap := make(map[int][]int)
	// initialize min and max to +Inf and -Inf respectively
	minEventTimeSinceZero := math.Inf(1)
	maxEventTimeSinceZero := math.Inf(-1)
	for i := 0; i < len(selectedEvents); i++ {
		// parse the timestamp of each event from the input
		// based on the input layout
		myDate, err := time.Parse(inputTimeLayout, selectedEvents[i].Timestamp)
		if err != nil {
			panic(err)
		}
		// calculate the elapsed time, in minutes, between the event
		// and time zero
		eventTimeSinceZero := myDate.Sub(zeroDate).Minutes()

		// min and max will be used to know which events
		// timestamps are the first and last
		// compute the minimum elapsed time associated
		// with the event with the lowest timestamp
		minEventTimeSinceZero = math.Min(minEventTimeSinceZero, eventTimeSinceZero)
		// compute the maximum elapsed time associated
		// with the event with the highest timestamp
		maxEventTimeSinceZero = math.Max(maxEventTimeSinceZero, eventTimeSinceZero+1)

		// append the duration associated with the event
		delivPerMinMap[int(minEventTimeSinceZero)] = append(delivPerMinMap[int(minEventTimeSinceZero)], 0)
		// loop based on the given window (default 10) and append the duration of the event
		// with the next events included in that window (next 10 events by default)
		for j := 1; j <= window; j++ {
			delivPerMinMap[int(eventTimeSinceZero)+j] = append(delivPerMinMap[int(eventTimeSinceZero)+j], selectedEvents[i].Duration)
		}
	}
	// return the populated map, min and max
	return delivPerMinMap, int(minEventTimeSinceZero), int(maxEventTimeSinceZero)
}

// select events based on command line args (default "") for
// client name, source language, target language and event name
func selectEvents(events []Event, clientName string, sourceLang string, targetLang string, eventName string) []Event {
	var selectedEvents []Event
	// loop on all events and select the ones where a command line argument
	// for a certain attribute is not ""
	// if it is not provided it is ignored
	for i := 0; i < len(events); i++ {
		if ((clientName == "") != (events[i].CliName == clientName)) && ((sourceLang == "") != (events[i].SourceLang == sourceLang)) && ((targetLang == "") != (events[i].TargetLang == targetLang)) && ((eventName == "") != (events[i].EventName == eventName)) {
			selectedEvents = append(selectedEvents, events[i])
		}
	}
	// returned the events
	return selectedEvents
}

//!-
