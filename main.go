package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"time"
)

type Event struct {
	Timestamp        string `json:"timestamp"`
	TranslationID    string `json:"translation_id"`
	SourceLanguage   string `json:"source_language"`
	TargetLanguage   string `json:"target_language"`
	ClientName       string `json:"client_name"`
	EventName        string `json:"event_name"`
	NrWords          int    `json:"nr_words"`
	Duration         int    `json:"duration"`
	ProcessedTimeMin string
}

func parseTimestamp(timestamp string) (time.Time, error) {
	t, err := time.Parse("2006-01-02 15:04:05.000000", timestamp)
	if err != nil {
		return time.Time{}, fmt.Errorf("Error parsing timestamp: %v", err)
	}
	return t, nil
}

func parseInputArgs() (string, int, error) {
	var fileName string
	var windowSize int
	flag.StringVar(&fileName, "input_file", "", "Input file name")
	flag.IntVar(&windowSize, "window_size", 0, "Window size in minutes")
	flag.Parse()

	if fileName == "" {
		return "", 0, fmt.Errorf("Input file name is required\n")
	}

	if windowSize == 0 {
		return "", 0, fmt.Errorf("Window size is required\n")
	}

	fmt.Println("Input file name:", fileName)
	fmt.Println("Window size:", windowSize)
	return fileName, windowSize, nil
}

func readEventsFromFile(fileName string) ([]Event, error) {
	file, err := os.Open(fileName)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var events []Event
	for scanner.Scan() {
		var event Event
		err := json.Unmarshal(scanner.Bytes(), &event)
		if err != nil {
			return nil, fmt.Errorf("Error decoding json: %v", err)
		}

		t, err := parseTimestamp(event.Timestamp)
		if err != nil {
			return nil, fmt.Errorf("Error parsing timestamp: %v", err)
		}

		event.ProcessedTimeMin = t.Format("2006-01-02 15:04:00")
		events = append(events, event)
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("Error reading file: %v", err)
	}

	return events, nil
}

func main() {
	fileName, _, err := parseInputArgs()
	if err != nil {
		fmt.Printf("Failed to parse input arguments: %v", err.Error())
		os.Exit(1)
	}

	events, err := readEventsFromFile(fileName)
	if err != nil {
		fmt.Printf("Failed to read events from the file: %v", err.Error())
		os.Exit(1)
	}

	for _, event := range events {
		fmt.Printf("%v\n", event)
	}
}
