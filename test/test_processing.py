import pytest
from collections import defaultdict
from datetime import datetime

from unbabel.processing import process_input
from unbabel.util import input_to_json, map_tuplelist

date_average = [(datetime(2018, 12, 26, 18, 11), 0), (datetime(2018, 12, 26, 18, 12), 20), (datetime(2018, 12, 26, 18, 13), 20), (datetime(2018, 12, 26, 18, 14), 20), (datetime(2018, 12, 26, 18, 15), 20), (datetime(2018, 12, 26, 18, 16), 25.5), (datetime(2018, 12, 26, 18, 17), 25.5), (datetime(2018, 12, 26, 18, 18), 25.5), (datetime(2018, 12, 26, 18, 19), 25.5), (datetime(2018, 12, 26, 18, 20), 25.5), (datetime(2018, 12, 26, 18, 21), 25.5), (datetime(2018, 12, 26, 18, 22), 25.5), (datetime(2018, 12, 26, 18, 23), 25.5), (datetime(2018, 12, 26, 18, 24), 39.75)]

test_input = [[('date', datetime(2018, 12, 26, 18, 11)),('average_delivery_time', 20)], [('date', datetime(2018, 12, 26, 18, 15)),('average_delivery_time', 31)], [('date', datetime(2018, 12, 26, 18, 23)),('average_delivery_time', 54)]]

process_test_data = [
    (
        [
            '{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}',
            '{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}',
            '{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}',
        ],
        14,
        defaultdict(None, date_average)
    ),
    ([], 1, defaultdict()),
    ([], 10, defaultdict()),
    ([], 100, defaultdict()),
    (None, 10, defaultdict()),
]

input_test_data = [
    (
        [
            '{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}',
            '{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}',
            '{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}',
        ],
        list(map(map_tuplelist, test_input))
    ),
    (None, []),
    ([], []),
]


@pytest.mark.parametrize('input,window_size,expected', process_test_data)
def test_correct_processing(input, window_size, expected):
    processed_data = process_input(input_to_json(input), window_size)
    assert processed_data == expected


@pytest.mark.parametrize('input, expected', input_test_data)
def test_input_to_json(input, expected):
    json_input = input_to_json(input)
    assert json_input == expected

