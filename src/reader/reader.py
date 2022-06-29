import json
from src.util.validation import validation_json_schema


def read(input_file):
    f = open(input_file)
    data = json.load(f)
    return validation_json_schema(data)
