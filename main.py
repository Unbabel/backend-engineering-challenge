from src.reader import read
from src.processor import process
import argparse


# Press the green button in the gutter to run the script.
# For each iteration I'll have the current timestamp - window size
# every minute will compare:
# 1. if no data available avg_delivered_time = 0
# 2. if data is available I have to track how many translation already happened and sum the time of those translations
# to get the avg
# 3. handle edge cases
# 4. create output
# 4. unit tests

def read_arguments():
    parser = argparse.ArgumentParser(description='Events Aggregated per minute')
    parser.add_argument('--input_file', required=True, type=str, help='Input file')
    parser.add_argument('--window_size', required=True, type=int, help='Window Size')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # args = read_arguments()
    args = {
        "input_file": 'files/events.json',
        "window_size": 10
    }
    df = read(args['input_file'])
    out_frame = process(df, args['window_size'])
    # write(out_frame)
