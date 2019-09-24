import argparse
from src.loading import load_timestamps


def create_arg_parser() -> argparse.ArgumentParser:
    """Parse the command line arguments for the unbabel_cli script."""

    parser = argparse.ArgumentParser(
        prog="Unbabel CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input_file",
        required=True,
        help="Path to the events JSON file",
    )

    parser.add_argument(
        "-w",
        "--window_size",
        required=True,
        type=int,
        help="Size of the window to compute the moving average",
    )

    return parser


if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()

    data = load_timestamps(args.input_file)
