import argparse
from src.event_processor.event_processor import process_events


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
    process_events(args.input_file, args.window_size)
    print("Operation Completed!")


if __name__ == '__main__':
    main()
