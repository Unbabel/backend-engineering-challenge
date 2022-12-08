from datetime import datetime, timedelta
from typing import List
from src.event_reader.event_reader import read_events
from src.util.utils import get_starting_window_datetime, sort_by_datetime, get_ending_window_datetime, write_to_file

"""
    Function that takes a Json file and a window size as input and produces
    a moving average by minute. moving average data are then saved on to a file

    params:
    fileName: name of the file to parse (str)
    window_size: dimensions of the window to take into consideration (int)

    output:
    a stream of events
"""


def process_events(file_name: str, window_size: int):
    events_list = read_events(file_name=file_name)
    sort_by_datetime(events_list)
    start_date = get_starting_window_datetime(events_list)
    _calculate_moving_average(events_list, window_size, start_date)


"""
    internal function that calculates the average for every time period
"""


def _calculate_moving_average(event_list: List[str], window_size: int, start_date: datetime):
    for diff in range(window_size + 1):
        period_date = get_ending_window_datetime(start_date, diff)
        filtered_events = list(filter(
            lambda x: x.timestamp <= period_date, event_list))
        if filtered_events:
            average = sum(i.duration for i in filtered_events) / \
                len(filtered_events)
        else:
            average = 0
        write_to_file(period_date, average)
