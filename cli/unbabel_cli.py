import argparse
import pandas as pd
from services.moving_average_service import MovingAverageService
from services.generate_output_service import GenerateOutputService
from services.process_data_service import ProcessDataService
from handlers.event_handler import EventHandler


def main():
    parser = argparse.ArgumentParser(
        prog='Command that parses a stream of events and calculating, for every minute, a moving average of the translation delivery time for the last X minutes.'
        )

    parser.add_argument('--input_file', type=str, help='path to file where events are stored', required=True)    
    parser.add_argument('-w', '--window_size', type=str, help='window size of moving average', required=True)
    args = parser.parse_args()

    df = EventHandler.convert_file_to_df(args.input_file)
    df = ProcessDataService.group_data_by_freq(df)
    df = MovingAverageService.simple_moving_average(df, int(args.window_size))
    GenerateOutputService.create_json_file(df)


if __name__ == '__main__':
    main()