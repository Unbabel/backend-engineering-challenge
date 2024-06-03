import json
import argparse
from datetime import datetime, timedelta

# Function to parse each event from JSON format
def parse_event(event):
    return {
        'timestamp': datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),
        'duration': event['duration']
    }

# Function to calculate the moving average delivery time
def moving_average(events, window_size):
    # Sort events based on timestamp
    events = sorted(events, key=lambda x: x['timestamp'])
    # Define start and end times of the event stream
    start_time = events[0]['timestamp'].replace(second=0, microsecond=0)
    end_time = events[-1]['timestamp'].replace(second=0, microsecond=0) + timedelta(minutes=1)
    # Define the window size
    window = timedelta(minutes=window_size)
    result = []

    # Loop through each minute in the event stream
    current_time = start_time
    while current_time <= end_time:
        # Calculate the start of the current window
        window_start = current_time - window + timedelta(minutes=1)
        # Extract events within the current window
        window_events = [event['duration'] for event in events if window_start <= event['timestamp'] <= current_time]
        # Calculate the average delivery time for the events within the window
        if window_events:
            avg_duration = sum(window_events) / len(window_events)
        else:
            avg_duration = 0
        # Append the result to the output list
        result.append({'date': current_time.strftime('%Y-%m-%d %H:%M:%S'), 'average_delivery_time': avg_duration})
        # Move to the next minute
        current_time += timedelta(minutes=1)

    return result



# Main function to read input, calculate moving average, and write output
def main(input_file, window_size):
    try:
        # Read events from the input file
        events = []
        with open(input_file, 'r') as file:
            for line in file:
                try:
                    # Parse each line as JSON and append to events list
                    event = json.loads(line.strip())
                    events.append(parse_event(event))
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in input file: {e}")
        
        # Check if events list is empty
        if not events:
            raise ValueError("Input file is empty")
        
        # Check if window size is valid
        if not isinstance(window_size, int) or window_size <= 0:
            raise ValueError("Window size must be a positive integer")

        # Calculate moving average delivery time
        averages = moving_average(events, window_size)

        # Write output to file
        with open('output.json', 'w') as file:
            for avg in averages:
                file.write(json.dumps(avg) + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except ValueError as e:
        print(f"Error: {e}")


# Command line argument parsing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process translation delivery events.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input JSON file with events.')
    parser.add_argument('--window_size', type=int, required=True, help='Size of the moving average window in minutes.')

    args = parser.parse_args()
    # Call main function with provided arguments
    main(args.input_file, args.window_size)
