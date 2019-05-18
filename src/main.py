#!/usr/bin/env python3

import argparse
from .reader import file_input_reader
from .metrics import Metrics

def main():
    parser = argparse.ArgumentParser(description='translation metrics generator for Unbabel backend challenge')
    parser.add_argument('--input_file', help='input filename', required=True)
    parser.add_argument('--window_size', type=int, help='age of entries to keep track of (minutes)', required=True)

    args = parser.parse_args()

    source = file_input_reader(args.input_file)
    metrics = Metrics(source, args.window_size)
    metrics.run()

if __name__ == "__main__":
    main()

import pytest

def test_basic():
    source = file_input_reader('./test_cases/basic.json')
    metrics = Metrics(source, 10, True)
    metrics.run()
    assert metrics.buffer[0] == {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0.0}
    assert metrics.buffer[-1] == {'date': '2018-12-26 18:23:00', 'average_delivery_time': 42.5}

def test_invalid():
    for file_name in ('empty', 'malformed', 'out_of_order', 'wrong_type'):
        source = file_input_reader('./test_cases/{}.json'.format(file_name))
        metrics = Metrics(source, 10, True)
        print(file_name)
        with pytest.raises(AssertionError):
            metrics.run()

# TODO: more test cases, fuzzing