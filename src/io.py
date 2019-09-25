import json
from typing import Text, List, Dict, Any
from pandas import DataFrame
from datetime import datetime
import logging

INPUT_TIMESTAMP_STR = "%Y-%m-%d %H:%M:%S.%f"
OUTPUT_TIMESTAMP_STR = "%Y-%m-%d %H:%M:%S"


class UnknownFormatError(BaseException):
    """Error raised when input file is not JSON standard."""

    def __init__(self, filepath: Text, error: json.JSONDecodeError):
        self.filepath = filepath
        self.error = error

    def __str__(self):
        message = (
            "Failed to load file '{}' because it is not in valid JSON format."
            "More info: {}"
        )
        return message.format(self.filepath, self.error)


def load_events(filepath: Text) -> DataFrame:
    """Loads event data from a JSON file."""

    try:
        events = _read_json(filepath)
    except json.JSONDecodeError as e:
        raise UnknownFormatError(filepath, e)

    events_df = _build_dataframe(events)
    logging.info("Loaded {} events from '{}'".format(len(events_df), filepath))

    return events_df


def _read_json(filepath: Text) -> List[Dict[Text, Any]]:
    """Reads lines from JSON and converts timestamps to datetimes."""
    events = []

    with open(filepath, "r") as f:
        for line in f.readlines():
            event = json.loads(line)
            event["timestamp"] = datetime.strptime(
                event["timestamp"], INPUT_TIMESTAMP_STR
            )
            events.append(event)

    return events


def _build_dataframe(events: List[Dict[Text, Any]]) -> DataFrame:
    """Converts timestamps to datetimes and returns a DataFrame."""

    events_df = DataFrame(data=events)
    events_df["timestamp"] = events_df["timestamp"].astype(datetime)

    return events_df


def export_averages(averages: List[Dict[Text, Any]], filepath: Text):
    """Write averages to file in the format we expect."""

    filestr = _format_file_string(averages)

    with open(filepath, "w+") as f:
        f.write(filestr)

    logging.info("Dumped {} averages to '{}'".format(len(averages), filepath))


def _format_file_string(averages: List[Dict[Text, Any]]) -> Text:
    """Converts datetimes to strings and removes floating zeroes."""

    filestr = ""

    for avg in averages:
        avg["date"] = datetime.strftime(avg["date"], OUTPUT_TIMESTAMP_STR)

        if avg["average_delivery_time"] % 1 == 0:
            avg["average_delivery_time"] = int(avg["average_delivery_time"])

        filestr += json.dumps(avg) + "\n"

    return filestr.rstrip("\n")
