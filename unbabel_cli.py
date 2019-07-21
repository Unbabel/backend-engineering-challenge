import argparse
import datetime
import json

import pandas as pd


class UnbabelCLI(object):
    """
    Parses a stream of events and produces an aggregated output
    """

    def __init__(self, input_file, window_size, output_file='output.json'):
        self.input_file = input_file
        self.window_size = window_size
        self.output_file = output_file

    def _get_dataframe_data(self):
        """
        read the file and return a DataFrame representation
        """
        data = []
        with open(self.input_file, 'r') as f:
            for event in f:
                data.append(json.loads(event))
        sorted_data = sorted(data, key=lambda i: datetime.datetime.strptime(
            i['timestamp'], '%Y-%m-%d %H:%M:%S.%f'))
        df = pd.DataFrame(sorted_data, columns=['timestamp', 'duration'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def _prepare_data(self, df):
        """
        Prepare a resampled data
        https://towardsdatascience.com/basic-time-series-manipulation-with-pandas-4432afee64ea
        https://www.kaggle.com/thebrownviking20/everything-you-can-do-with-a-time-series
        """
        df = df.set_index('timestamp')
        min_ = df.index.min()
        max_ = df.index.max()
        df = df.resample('min', closed='left', label='right').mean()
        new_rage = pd.date_range(min_.floor('min'), max_.ceil('min'),
                                 freq='1min')
        df = df.reindex(new_rage)
        return df

    def generate_moving_averages(self):
        """
        Given a dataframe, generates the moving averages
        """
        df = self._get_dataframe_data()
        df = self._prepare_data(df)
        df['average_delivery_time'] = df.rolling(self.window_size,
                                                 min_periods=1).mean().fillna(0)
        del df['duration']
        df = df.fillna(0)
        df = df.reset_index()
        df.rename(columns={'index': 'date'}, inplace=True)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        results = df.to_dict(orient='records')
        with open(self.output_file, 'w') as f:
            for result in results:
                f.write(str(result) + '\n')
        return df


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--input_file',
                            help='File path containing the events',
                            required=True)
    arg_parser.add_argument('-w', '--window_size', help='Past minutes',
                            required=True, type=int)
    arg_parser.add_argument('-o', '--output_file',
                            help='File path storing aggregated data',
                            required=False)
    args = arg_parser.parse_args()
    output_file = args.output_file or 'output_file.json'
    unbabel_cli = UnbabelCLI(args.input_file, args.window_size, output_file)
    unbabel_cli.generate_moving_averages()
