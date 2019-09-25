import json
from typing import Text, List, Dict, Any, Optional
from pandas import DataFrame
from datetime import datetime
import logging
import os

INPUT_TIMESTAMP_STR = "%Y-%m-%d %H:%M:%S.%f"
OUTPUT_TIMESTAMP_STR = "%Y-%m-%d %H:%M:%S"

EXPECTED_KEYS = (
    "timestamp",
    "translation_id",
    "source_language",
    "target_language",
    "client_name",
    "event_name",
    "nr_words",
    "duration",
)


class UnknownFormatError(BaseException):
    """Error raised when input file is not standard."""

    def __init__(self, filepath: Text, reason: Text):
        self.filepath = filepath
        self.reason = reason

    def __str__(self):
        message = "Failed to load file '{}' because ".format(self.filepath)
        return message + self.reason


def load_events(filepath: Text) -> DataFrame:
    """Loads event data from a JSON file."""

    events = _read_json(filepath)

    events_df = _build_dataframe(events)
    logging.info("Loaded {} events from '{}'".format(len(events_df), filepath))

    return events_df


def _validate(i: int, line: Text, filepath: Text):
    """Asserts that each line from the input file is in the correct format."""

    # assert event is JSON-readable
    event = json.loads(line)

    # assert event is not missing mandatory keys
    for key in EXPECTED_KEYS:
        if key not in event.keys():
            raise UnknownFormatError(
                filepath,
                reason="line {} is missing expected events key '{}'".format(i, key),
            )

    # assert event timestamp is in correct format
    try:
        event["timestamp"] = datetime.strptime(event["timestamp"], INPUT_TIMESTAMP_STR)
    except ValueError:
        raise UnknownFormatError(
            filepath,
            reason="line {} contains a timestamp which is not in the format {}".format(
                i, INPUT_TIMESTAMP_STR
            ),
        )

    return event


def _read_json(filepath: Text) -> List[Dict[Text, Any]]:
    """Reads lines from JSON and converts timestamps to datetimes."""
    events = []

    with open(filepath, "r") as f:
        for i, line in enumerate(f.readlines()):
            event = _validate(i, line, filepath)
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

    filepath = os.path.abspath(filepath)
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
