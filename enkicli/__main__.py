import argparse

from enki.JsonDumper import JsonDumper
from enki.JsonParser import JsonParser
from enki.PerMinuteMovingAverageCalculator import PerMinuteMovingAverageCalculator
from enki.ProcessorChain import ProcessorChain


def main():
    parser = argparse.ArgumentParser(
        prog='enki',
        description='enki - translation event processor')
    parser.add_argument('--input_file', type=str, required=True,
                        help='input file name, jsonl')
    parser.add_argument('--window_size', type=int, required=True,
                        help='moving average window size')

    args = parser.parse_args()

    process(args.input_file, args.window_size)


def process(input_file: str, window_size: int):
    chain = ProcessorChain(print,
                           [
                               lambda sink: JsonParser(sink),
                               lambda sink: PerMinuteMovingAverageCalculator(
                                   sink,
                                   window_size,
                                   lambda x: "%s:00" % x["timestamp"][:16],
                                   lambda x: x["duration"], "date", "average_delivery_time"),
                               lambda sink: JsonDumper(sink),
                           ])

    with open(input_file, 'rt') as f:
        for line in f:
            chain.consume(line)

    chain.end()


if __name__ == '__main__':
    main()
