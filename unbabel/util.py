import json
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import islice
import os.path


INPUT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
OUTPUT_FORMAT = "%Y-%m-%d %H:%M:%S"


class JSONEncoder(json.JSONEncoder):
    """JSON encoder that handles dates (serialized in specified format)"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(OUTPUT_FORMAT)


def map_output(output):
    return json.dumps(output, cls=JSONEncoder)


def map_input(input):
    """ formats the input into working format
        for input:
            {
                'timestamp': '2018-12-26 18:11:08.509654', 'translation_id': '5aa5b2f39f7254a75aa5',
                'source_language': 'en', 'target_language': 'fr', 'client_name': 'easyjet',
                'event_name': 'translation_delivered', 'nr_words': 30, 'duration': 20
            }
        output will be:
            defaultdict(None, {'date': datetime.datetime(2018, 12, 26, 18, 11), 'duration': 20})

        :param input: dictionary of line of input
        :return: line mapped into dictionary with date as the timestamp value of input converted to string and truncated seconds and miliseconsd and duration as the input duration field
    """
    formatted_input = defaultdict()
    if input and "timestamp" in input.keys() and "duration" in input.keys():
        formatted_input["date"] = datetime.strptime(
            input["timestamp"], INPUT_FORMAT
        ).replace(second=0, microsecond=0)
        formatted_input["average_delivery_time"] = input["duration"]
    return formatted_input


def get_entry_date(input):
    """
    Gets the date of the event and the effective date for which to count duration for
    Input format:
        defaultdict(None, {'date': datetime.datetime(2018, 12, 26, 18, 11), 'duration': 20})
    :param input: list of input dictionaries
    :return: datetime object of timestamp value
    """
    if input and "date" in input.keys():
        return input["date"], input["date"] + timedelta(minutes=1)
    return None, None


def prop_data(input_data):
    return list(map(map_input, list(map(json.loads, input_data))))


def print_data(formatted_data):
    for date, average in formatted_data.items():
        print(
            json.dumps(
                {"date": date, "average_delivery_time": average}, cls=JSONEncoder
            )
        )


def load_file(file_name, window_size):
    with open(file_name, "r") as input_file:
        cache = islice(input_file, window_size)
        return list(map(str.rstrip, cache))


def input_to_json(input):
    if input:
        return list(map(map_input, list(map(json.loads, input))))
    return []


def valid_file(file_name):
    return os.path.exists(file_name) and os.path.isfile(file_name)


def map_tuplelist(tuplelist):
    return defaultdict(None, tuplelist)
