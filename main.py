import argparse
import json
from datetime import datetime, timedelta

def calculate_moving_average(input_file, window_size):
    event_queue = []
    average_delivery_times = []
    if input_file:
        with open(input_file, 'r') as file:
            events = [json.loads(line) for line in file]
        # print(events)
    for event in events:
        timestamp = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        duration =  event['duration']
        event_queue.append((timestamp, duration))
        while event_queue and timestamp - event_queue[0][0] > timedelta(minutes=window_size):
            event_queue.pop(0)
        # print(f"After while loop - event_queue: {event_queue}")
        # Calculate moving averages for each minute within the current time window
        current_time = timestamp
        window_start_time = current_time - timedelta(minutes=window_size)

        while event_queue and event_queue[0][0] < current_time:
            # Filter events within the current time window [current_minute - window_size, current_minute]
            events_within_window = [(time, duration) for time, duration in event_queue if window_start_time <= time <= current_time]
            print('them evts', events_within_window)
            # Calculate moving average only if there are events within the window
            if events_within_window:
                moving_average = round(sum(duration for _, duration in events_within_window) / len(events_within_window), 2)
            else:
                moving_average = 0

            average_delivery_times.append({"date": current_time.strftime('%Y-%m-%d %H:%M:%S'), "average_delivery_time": moving_average})

            # Move the time window to the next minute
            current_time -= timedelta(minutes=1)
            window_start_time = current_time - timedelta(minutes=window_size)  # Update the window start time

        # print(average_delivery_times)
        
    save_to_file(average_time=average_delivery_times)

def save_to_file(average_time):
    
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
    