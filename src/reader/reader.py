import json
from src.util.validation import validation_json_schema


def read(input_file):
    f = open(input_file)
    events = json.load(f)
    validation_json_schema(events)
    return events;
