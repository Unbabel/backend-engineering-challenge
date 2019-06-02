import argparse
import json
from datetime import datetime

import pandas as pd

COLUMNS = ['timestamp', 'duration', 'nr_words', 'source_language', 'target_language', 'client_name']


def evaluate(intake):
    file_data = []

    with open(intake.input_file, 'r') as fd:
        for line in fd:
            file_data.append(json.loads(line))

    # sorts the file_data
    sorts = sorted(file_data, key=lambda z: datetime.strptime(z['timestamp'], '%Y-%m-%d %H:%M:%S.%f'), reverse=False)
    dfr = pd.DataFrame(sorts, columns=COLUMNS)

    dfr['timestamp'] = pd.to_datetime(dfr.timestamp)
    dfr = dfr.set_index('timestamp')

    starts, ends = dfr.index.min().floor('min'), dfr.index.max().ceil('min')

    # filter by a client's name if supplied
    if intake.client_name is not None:
        dfr = dfr[dfr.client_name == intake.client_name]

    dfr = dfr[['duration']].resample('min', label='right', closed='left').mean()  # re-sample the data
    dfr = dfr.reindex(pd.date_range(starts, ends, freq='1min').rename('date'))

    dfr['average_delivery_time'] = dfr[['duration']].rolling(intake.window_size, min_periods=1).mean().round(2)
    dfr = dfr[['average_delivery_time']]
    dfr = dfr.fillna(0)
    dfr = dfr.reset_index()

    dfr['date'] = dfr['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    result = '\n'.join([json.dumps(_) for _ in dfr.to_dict(orient='records')])

    if intake.output_file is not None:
        with open(intake.output_file, 'w') as response_file:
            response_file.write(result)
    else:
        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', required=True, type=str)
    parser.add_argument('--window_size', required=True, type=int)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--client_name', type=str)

    evaluate(parser.parse_args())
