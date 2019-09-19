# Unbabel Command Line Application

This command line application parses a stream of events and produces an aggregated output.

Aggregated output contains, for every minute, a moving average of the translation delivery time for the last X minutes.

## How to Run?

- Clone this repository `git clone https://github.com/noraiz-anwar/backend-engineering-challenge.git`
- Go to folder `cd backend-engineering-challenge`
- run `[python 3] unbabel_cli.py --input_file [path to .json file] --window_size [number of minutes] [filter arguments]`

### _Examples:_

_events.json is in same directory as unbabel_cli.py in these examples._

- `python3 unbabel_cli.py --input_file events.json --window_size 10`
- `python3 unbabel_cli.py --input_file events.json --window_size 10 --client_name booking`
- `python3 unbabel_cli.py --input_file events.json --window_size 10 --client_name easyjet --source_language en`
- `python3 unbabel_cli.py` (defaults: input_file=events.json and window_size=10)

## What is here for extra points :)

Running average can also be calculated based on any valid key:value filtering of events.

**For example:**

- `python3 unbabel_cli.py --input_file events.json --window_size 10 --client_name booking`

Calculates, for every minute, running average for last 10 minutes of events for "booking" client.

## Considerations:

**unbabel_cli** considers that:

- Events in input file are sorted in ascending order of time.
- App was tested on Python 3.6.0
