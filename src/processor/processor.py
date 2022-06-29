import datetime

import pandas as pd


def process(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    return __calculate_moving_average(df, window_size)


# For every window of x minutes will create a dataframe of [dates,duration]
# Will filter the selected records for corresponding window [dates,duration]
# calculates the moving average with rolling function [dates, avg]
# return a master dataframe of the output
def __calculate_moving_average(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    df['dates'] = df['timestamp'].astype('datetime64[s]')
    df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M:%S.%f')
    df2 = df[['dates', 'duration']]
    start_time = df2['dates'].dt.round('min').min()
    end_time = df2['dates'].dt.round('min').max()
    date_ranges = _generate_dates(end_time, start_time)
    all_df = pd.concat([df2, date_ranges])
    all_df = all_df.sort_values('dates')
    moving_average_df = all_df.rolling(str(window_size) + 'min', on='dates').mean().resample('1min', on='dates').first()
    moving_average_df['duration'] = moving_average_df['duration'].fillna(0)
    return moving_average_df


def _generate_dates(end_time, start_time):
    return pd.DataFrame(pd.date_range(start=start_time - datetime.timedelta(minutes=1),
                                      end=end_time + datetime.timedelta(minutes=1), freq='min'),
                        columns=['dates'])
