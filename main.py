from typing import List, Dict, Union
import argparse
import json
from datetime import datetime, timedelta

def read_events_from_file(input_file: str) -> List[Dict]:
    """
    Read events from a JSON file and return a list of events.

    Parameters:
        input_file (str): Path to the input JSON file.

    Returns:
        list: List of event dictionaries.
    """
    events = []
    if input_file:
        with open(input_file, 'r') as file:
            events = [json.loads(line) for line in file]
    return events

def remove_old_events(event_queue: List[tuple], timestamp: datetime, window_size: int) -> None:
    """
    Remove events outside the current time window from the event queue.

    Parameters:
        event_queue (list): List of tuples containing (timestamp, duration).
        timestamp (datetime): Current event timestamp.
        window_size (int): Size of the time window for moving average.
    """
    while event_queue and timestamp - event_queue[0][0] > timedelta(minutes=window_size):
        event_queue.pop(0)

def filter_events_within_window(event_queue: List[tuple], window_start_time: datetime, current_time: datetime) -> List[tuple]:
    """
    Filter events within the current time window.

    Parameters:
        event_queue (list): List of tuples containing (timestamp, duration).
        window_start_time (datetime): Start time of the current window.
        current_time (datetime): Current time.

    Returns:
        list: List of tuples containing (timestamp, duration) within the window.
    """
    return [(time, duration) for time, duration in event_queue if window_start_time <= time <= current_time]

def calculate_moving_average(input_file: str, window_size: int) -> None:
    """
    Calculate moving average delivery time.

    Parameters:
        input_file (str): Path to the input JSON file.
        window_size (int): Size of the time window for moving average.
    """
    event_queue: List[tuple] = []
    average_delivery_times: List[Dict[str, Union[str, float]]] = []

    events = read_events_from_file(input_file)

    for event in events:
        timestamp = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        duration = event['duration']
        event_queue.append((timestamp, duration))

        remove_old_events(event_queue, timestamp, window_size)

        current_time = timestamp
        window_start_time = current_time - timedelta(minutes=window_size)

        while event_queue and event_queue[0][0] < current_time:
            events_within_window = filter_events_within_window(event_queue, window_start_time, current_time)

            if events_within_window:
                moving_average = round(sum(duration for _, duration in events_within_window) / len(events_within_window), 2)
            else:
                moving_average = 0

            average_delivery_times.append({"date": current_time.strftime('%Y-%m-%d %H:%M:%S'), "average_delivery_time": moving_average})

            current_time -= timedelta(minutes=1)
            window_start_time = current_time - timedelta(minutes=window_size)

    save_to_file(average_delivery_times)

def save_to_file(average_time: List[Dict[str, Union[str, float]]]) -> None:
    """
    Save moving average delivery times to a file and print them.

    Parameters:
        average_time (list): List of dictionaries containing date and average delivery time.
    """
    average_time.sort(key=lambda x: x["date"])
    for mv in average_time:
        print(mv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate moving average delivery time.')
    parser.add_argument('--input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, help='Size of the time window for moving average')
    args = parser.parse_args()
    input_file, window_size = args.input_file, args.window_size
    calculate_moving_average(input_file=input_file, window_size=window_size)
