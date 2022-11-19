import argparse
import pandas as pd
from services.moving_average_service import MovingAverageService
from services.generate_output_service import GenerateOutputService
from services.process_data_service import ProcessDataService
from handlers.event_handler import EventHandler


def main():
    parser = argparse.ArgumentParser(prog='Unbabel\'s command parser')

    parser.add_argument('--input_file')    
    parser.add_argument('-w', '--window_size')
    args = parser.parse_args()

    df = EventHandler.convert_file_to_df(args.input_file)
    df = ProcessDataService.group_data_by_freq(df)
    df = MovingAverageService.simple_moving_average(df, int(args.window_size))
    GenerateOutputService.create_json_file(df)


if __name__ == '__main__':
    main()