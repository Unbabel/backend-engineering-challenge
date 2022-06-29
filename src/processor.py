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
    df2 = df[['dates', 'duration']]
    start_time = df2['dates'].dt.round('min').min()
    dummy_df = pd.DataFrame(pd.date_range(start=start_time,
                                          end=start_time + datetime.timedelta(minutes=window_size), freq='min'),
                            columns=['dates'])
    dummy_df['duration'] = 0
    selected_records = df2[df2['dates'].between(start_time, start_time + datetime.timedelta(minutes=window_size))]
    merged_df = pd.concat([dummy_df, selected_records])
    merged_df.resample
#
#   2018-12-26 18:12:00, 0.0
#   2018-12-26 18:12:07, 20.0
#   2018-12-26 18:13:00, 0.0
#   2018-12-26 18:14:00, 0.0
#   2018-12-26 18:14:10, 20.0
#   2018-12-26 18:15:00, 0.0
