import json
from typing import Text, List
from datetime import datetime
import logging

INPUT_TIMESTAMP_STR = "%Y-%m-%d %H:%M:%S.%f"


class UnknownFormatError(BaseException):
    """Error raised when input file is not JSON standard."""

    def __init__(self, filepath: Text, error: json.JSONDecodeError):
        self.filepath = filepath
        self.error = error

    def __str__(self):
        message = (
            "Failed to load file '{}' because it is not in valid JSON format.  "
            "More info: {}"
        )
        return message.format(self.filepath, self.error)


class MissingTimestampsError(BaseException):
    """Error raised when the input file has no timestamps at all."""

    def __init__(self, filepath: Text):
        self.filepath = filepath

    def __str__(self):
        message = "File '{}' doesn't contain any timestamps."
        return message.format(self.filepath)


def load_timestamps(filepath: Text) -> List[datetime]:
    """Loads timestamps from an events file."""
    timestamps = []

    try:
        with open(filepath, "r") as f:
            for line in f.readlines():
                event = json.loads(line)
                timestamps.append(event.get("timestamp"))

    except json.JSONDecodeError as e:
        raise UnknownFormatError(filepath, e)

    if not any(timestamps):
        raise MissingTimestampsError(filepath)

    logging.info("Loaded {} events from '{}".format(len(timestamps), filepath))

    return [datetime.strptime(ts, INPUT_TIMESTAMP_STR) for ts in timestamps]
