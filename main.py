from src.reader.reader import read
from src.processor.processor import process
from src.writer.writer import write
import argparse


def read_arguments():
    parser = argparse.ArgumentParser(description='Events Aggregated per minute')
    parser.add_argument('--input_file', required=True, type=str, help='Input file')
    parser.add_argument('--window_size', required=True, type=int, help='Window Size')
    parser.add_argument('--output_file', required=True, type=str, help='Output file')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = read_arguments()
    events = read(args.input_file)
    moving_average_list = process(events, args.window_size)
    write(moving_average_list, args.output_file)
