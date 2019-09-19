
"""
Entry point into application.
"""


from src.event_getter import EventGetter
from src.aggregator import AverageAggregator

from src.file_operations import get_file_stream_to_read, get_file_stream_to_write, close_file_stream
from src.argument_parser import get_command_line_arguments


def main():
    """
    Calls application code.
    """
    input_file, window_size, filters = get_command_line_arguments()

    event_stream = get_file_stream_to_read(input_file)
    output_stream = get_file_stream_to_write()

    event_getter = EventGetter(event_stream, filters)
    events = event_getter.get_events()

    average_aggregator = AverageAggregator(
        events, window_size, output_stream
    )

    average_aggregator.create_per_minute_averages()

    event_stream.close()
    output_stream.close()


if __name__ == "__main__":
    main()
