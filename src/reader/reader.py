import json
from src.util.util import get_rounded_off_datetime, get_datetime_from_string
from src.util.validation import validation_json_schema


def read(input_file):
    f = open(input_file)
    events = json.load(f)
    validation_json_schema(events)
    for event in events:
        event['timestamp'] = get_datetime_from_string(event['timestamp'])
        event['datetime'] = get_rounded_off_datetime(event['timestamp'])
    return events;
