import argparse

from unbabel.util import valid_file, load_file, input_to_json, print_data
from unbabel.processing import process_input


def main(args):
    file_name = args.input_file
    window_size = args.window_size

    if not valid_file(file_name):
        print("ERROR: {} is not a valid file.".format(args.input_file))
    else:
        file_content = load_file(file_name, window_size)
        processed_input = process_input(input_to_json(file_content), window_size)
        print_data(processed_input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file", help="Path to the file to parse", type=str, required=True
    )
    parser.add_argument(
        "--window_size",
        help="Size of the window to print in minutes",
        type=int,
        required=True,
    )
    args = parser.parse_args()
    main(args)
