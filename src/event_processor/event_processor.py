from src.event_reader.event_reader import read_events
from src.util.utils import get_starting_window_datetime, sort_by_datetime, get_ending_window_datetime

"""
    Function that takes a Json file and a window size as input and produces
    a moving average by minute

    params:
    fileName: name of the file to parse (str)
    window_size: dimensions of the window to take into consideration (int)

    output:
    a stream of events
"""


def event_processor(file_name: str, window_size: int) -> str:
    events_list = read_events(file_name=file_name)
    sort_by_datetime(events_list)
    start_date = get_starting_window_datetime(events_list)
    end_date = get_ending_window_datetime(start_date, window_size)
