import argparse
from src.io import load_events, export_averages
from src.processing import moving_averages


def create_arg_parser() -> argparse.ArgumentParser:
    """Parse the command line arguments for the unbabel_cli script."""

    parser = argparse.ArgumentParser(
        prog="Unbabel CLI", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--input_file", required=True, help="Path to the events JSON file"
    )

    parser.add_argument(
        "-w",
        "--window_size",
        required=True,
        type=int,
        help="Size of the window to compute the moving average",
    )

    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    events = load_events(args.input_file)
    averages = moving_averages(events, args.window_size)
    export_averages(averages, "output.json")