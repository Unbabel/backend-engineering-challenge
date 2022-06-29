import datetime

import numpy as np
import pandas as pd


def process(df, window_size) -> pd.DataFrame:
    return _calculateAvg(df, window_size)


# For every window of x minutes will create a dataframe of [dates,duration]
# Will filter the selected records for corresponding window [dates,duration]
# calculates the moving average with rolling function [dates, avg]
# return a master dataframe of the output
def _calculateAvg(df, window_size) -> pd.DataFrame:
    df['dates'] = df['timestamp'].astype('datetime64[s]')
    df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M:%S.%f')
    df2 = df[['dates', 'duration']]
    start_time = df2['dates'].dt.round('min').min()
    dummy_df = pd.DataFrame(pd.date_range(start=start_time,
                                          end=start_time + datetime.timedelta(minutes=window_size), freq='min'),
                            columns=['dates'])
    all_df = pd.concat([df2, dummy_df])
    all_df = all_df.sort_values('dates')
    print(all_df.rolling(str(window_size) + 'min', on='dates').mean())
    selected_records = df2[df2['dates'].between(start_time, start_time + datetime.timedelta(minutes=window_size))]
