import argparse


def parse_args():
    args_parser = argparse.ArgumentParser(
        prog="event-cli"
        usage="Use --input-file argument to select an input file, use --window-size argument to define a size for the analyzed window")
    args_parser.add_argument(
        "--input-file", required=True, type=str, help="Name of the input file")
    args_parser.add_argument(
        "--window-size", required=True, type=int, help="Size of the window")
    args = args_parser.parse_args()
    return args


def main():
    args = parse_args()


if __name__ == '__main__':
    main()
