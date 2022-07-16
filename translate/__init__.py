from datetime import datetime
from translate.utils import (
    arguments_parser, convert_timestamps, read_file,
    add_minutes, set_seconds, applied_filter_on_data, 
    get_average, convert_datetime_to_string, write_file,
    convert_float_to_int
)

def data_processing(data: list, window_size: int) -> list:
    converted_data = convert_timestamps(data)
    start_date: datetime = set_seconds(converted_data[0]['timestamp'])
    end_date: datetime = add_minutes(set_seconds(converted_data[-1]['timestamp']))
    output_data: list = []

    while (end_date >= start_date):
        output: dict = {}
        filtered_data: list = applied_filter_on_data(start_date, converted_data, window_size)
        average: float = get_average(filtered_data)
        output['date'] = convert_datetime_to_string(start_date)
        output['average_delivery_time'] = convert_float_to_int(average)
        output_data.append(output)
        start_date = add_minutes(start_date)

    return output_data

def main() -> None:
    args = arguments_parser()
    data = read_file(args.input_file)
    output_data = data_processing(data, args.window_size)
    write_file("output.json", output_data)
