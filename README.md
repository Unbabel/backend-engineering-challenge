# Unbabel CLI Application
This is a pythonic command-line tool to parse and analyze translation delivery events in order to generate & report moving average delivery time every minute within a specified window size.

##Get Started
Run a help command to see all the command-line options the tool supports.

`python unbabel_cli.py --help`

Output:

```
usage: python unbabel_cli.py [-h] -i INPUT_FILE -w WINDOW_SIZE
                             [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Path to file containing delivery events
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        Number of past minutes to consider
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Path to file to store aggregated output data
```

##*Command-line Examples*
***Without an optional output file option:***

`python unbabel_cli.py --input_file events.json --window_size 13`

or

`python unbabel_cli.py -i events.json -w 13`



***With an optional output file option:***

`python unbabel_cli.py --input_file events.json --window_size 13 --output_file data.json`

or

`python unbabel_cli.py -i events.json -w 13 -o data.json`

##I/O Samples
Input file content:
```json
{"timestamp": "2018-12-26 18:11:00.000000","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 10, "duration": 10}
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}
{"timestamp": "2018-12-26 18:23:00.000000","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 200, "duration": 94}
```

Output file content:
```json
{"date": "2018-12-26 18:11:00", "average_delivery_time": 10}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 15}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 15}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 15}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 15}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 20.3}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 38.8}

```