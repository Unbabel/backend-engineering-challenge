import argparse
import json
import datetime as dt
from datetime import datetime

def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True, type=str)
    parser.add_argument('--window_size', required=True, type=int)
    return parser.parse_args()

def read_file(input_file) -> dict:
    with open(input_file, 'r') as file:
        return json.load(file)

def write_file(output_file, data) -> None:
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def convert_string_to_datetime(date: str, format='%Y-%m-%d %H:%M:%S.%f') -> datetime: 
    return datetime.strptime(date,format)

def convert_datetime_to_string(date: datetime, format='%Y-%m-%d %H:%M:%S') -> str:
    return date.strftime(format)

def add_minutes(date, minutes=1) -> datetime:
    return date + dt.timedelta(minutes=minutes)

def set_seconds(date, second=0, microsecond=0):
    return date.replace(second=second, microsecond=microsecond)

def convert_timestamps(data: list) -> list:
    for d in data:
        d['timestamp'] = convert_string_to_datetime(d['timestamp'])
    return data

def applied_filter_on_data(start_date: datetime, events: list, window_size: int) -> list:
    return list(filter(
        lambda event : event['timestamp'] < start_date and 
        add_minutes(event['timestamp'], window_size) > start_date, events
    ))

def get_average(data: list) -> float:
    return sum([i['duration'] for i in data ]) / len(data) if data else 0

def convert_float_to_int(data: float) -> int or float:
    return int(data) if not data % 1 else data 
