from reader import file_input_reader
from metrics import Metrics


if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(description='translation metrics generator for Unbabel backend challenge')
    # parser.add_argument('--input_file', help='input filename', required=True)
    # parser.add_argument('--window_size', type=int, help='age of entries to keep track of (minutes)', required=True)

    # args = parser.parse_args()
    # print(args)

    source = file_input_reader('../test/test.json')
    metrics = Metrics(source, 10)
    metrics.run()