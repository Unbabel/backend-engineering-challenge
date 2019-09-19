"""
"""

import argparse
from .settings import DEFAULT_INPUT_FILE, DEFAULT_WINDOW_SIZE


def get_command_line_arguments():

    argument_parser = argparse.ArgumentParser(
        description="Creates a running average for each minute."
    )

    argument_parser.add_argument(
        '--input_file',
        metavar='*.json',
        help='Path of a file which contains translation events',
        default=DEFAULT_INPUT_FILE
    )

    argument_parser.add_argument(
        '--window_size',
        metavar='N',
        type=int,
        help='Last number of minutes',
        default=DEFAULT_WINDOW_SIZE
    )

    __, unknown = argument_parser.parse_known_args()

    for arg in unknown:
        if arg.startswith(("-", "--")):
            argument_parser.add_argument(arg)

    arguments = argument_parser.parse_args()

    arguments = vars(arguments)

    input_file = arguments.pop('input_file')
    window_size = arguments.pop('window_size')

    if window_size < 0:
        argument_parser.error("Window size should be greater then 0")

    if not input_file.endswith('.json'):
        argument_parser.error("Path to a json file required")

    return input_file, window_size, arguments
