import argparse
from src.event_processor.event_processor import event_processor


def parse_args():
    args_parser = argparse.ArgumentParser(
        prog="event-cli",
        usage="Use --input_file argument to select an input file, use --window_size argument to define a size for the analyzed window")
    args_parser.add_argument(
        "--input_file", required=True, type=str, help="Name of the input file")
    args_parser.add_argument(
        "--window_size", required=True, type=int, help="Size of the window")
    args = args_parser.parse_args()
    return args


def main():
    args = parse_args()
    event_processor(args.input_file, args.window_size)


if __name__ == '__main__':
    main()
