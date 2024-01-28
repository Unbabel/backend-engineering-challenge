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
            
        if event_queue:
            moving_average = sum(duration for _, duration in event_queue) / len(event_queue)
            print(moving_average)
            average_delivery_times.append({'date': timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'average_delivery_time': moving_average})

    # save_to_file(average_time=average_delivery_times)

def save_to_file(average_time):
    for mv in average_time:
        print(mv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate moving average delivery time.')
    parser.add_argument('--input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, help='Size of the time window for moving average')
    args = parser.parse_args()
    input_file, window_size = args.input_file, args.window_size
    calculate_moving_average(input_file=input_file, window_size=window_size)
    