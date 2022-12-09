from datetime import datetime, timedelta
from src.event_reader.event_reader import read_events
from src.util.utils import get_starting_window_datetime, get_datetime_from_string, write_to_file

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
    start_date = get_starting_window_datetime(events_list)
    _calculate_moving_average(file_name, window_size, start_date)


"""
    Function that, for every minute starting from start_date, 
    calculates the moving average for the window defined by the param window_size

    params:
        event_list: iterator representing the list of events
        windows_size: parameter defining the dimensions of the window
        start_date: the start date of the period
"""


def _calculate_moving_average(file_name: str, window_size: int, start_date: datetime):
    for minute in range(0, window_size + 1):
        event_list = read_events(file_name=file_name)
        counter = 0
        total_duration = 0
        current_datetime = start_date + timedelta(minutes=minute)
        lower_bound = current_datetime - timedelta(minutes=window_size)
        for item in event_list:
            if (get_datetime_from_string(item["timestamp"]) < current_datetime) and (get_datetime_from_string(item["timestamp"]) > lower_bound):
                counter = counter + 1
                total_duration = total_duration + item["duration"]
        average_delivery_time = _calculate_average(
            total_duration, counter)
        write_to_file(period_date=current_datetime,
                      average=average_delivery_time)


"""
    Simple helper function to calculate average

    params:
        duration: sum of the durations
        counter: number of elements in the sequence
"""


def _calculate_average(duration: int, counter: int) -> float:
    if counter == 0:
        return 0
    else:
        return duration / counter
