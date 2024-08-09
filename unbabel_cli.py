#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timedelta
from collections import deque
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments for input file and window size."""
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery times.')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, required=True, help='Window size in minutes')
    return parser.parse_args()

def parse_timestamp(timestamp_str):
    """Convert timestamp string to a datetime object."""
    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError as e:
        logger.error(f"Timestamp parsing error: {e}")
        raise

def calculate_moving_average(input_file, window_size):
    """Calculate and print the moving average of delivery times."""
    window = deque()  # Initialize a deque to store events within the window
    current_minute = None  # Track the current minute being processed
    last_event_minute = None  # Track the last event's minute

    try:
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event = json.loads(line)  # Parse each line as a JSON event
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parsing error on line {line_num}: {e}")
                    continue

                timestamp = parse_timestamp(event['timestamp'])
                minute = timestamp.replace(second=0, microsecond=0)  # Round down to the nearest minute

                if current_minute is None:
                    current_minute = minute

                last_event_minute = minute

                # Process each minute up to the current event's minute
                while current_minute <= minute:
                    # Remove events that are outside the window
                    while window and (current_minute - parse_timestamp(window[0]['timestamp'])).total_seconds() / 60 >= window_size:
                        window.popleft()

                    # Calculate the average delivery time for the current minute
                    if window:
                        avg_delivery_time = sum(e['duration'] for e in window) / len(window)
                    else:
                        avg_delivery_time = 0

                    # Output the result for the current minute
                    print(json.dumps({
                        "date": current_minute.strftime("%Y-%m-%d %H:%M:%S"),
                        "average_delivery_time": round(avg_delivery_time, 1)
                    }))

                    current_minute += timedelta(minutes=1)

                # Add the current event to the window
                window.append(event)

        # Continue processing for the remaining minutes after the last event
        # This ensures we calculate the moving average for the entire window size after the last event
        while current_minute <= last_event_minute + timedelta(minutes=window_size):
            # Remove events that are outside the window
            while window and (current_minute - parse_timestamp(window[0]['timestamp'])).total_seconds() / 60 >= window_size:
                window.popleft()

            # Calculate the average delivery time for the current minute
            if window:
                avg_delivery_time = sum(e['duration'] for e in window) / len(window)
            else:
                avg_delivery_time = 0

            # Output the result for the current minute
            print(json.dumps({
                "date": current_minute.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": round(avg_delivery_time, 1)
            }))

            current_minute += timedelta(minutes=1)

    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def main():
    """Main function to parse arguments and calculate moving averages."""
    args = parse_arguments()
    calculate_moving_average(args.input_file, args.window_size)

if __name__ == "__main__":
    main()
