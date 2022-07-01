import datetime

import pandas as pd


def process(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    return __calculate_moving_average(df, window_size)


# Generates a dataframe of a date range from the start time to the end time of the input per minute
# It concat the dataframe of data range and input
# calculates the moving average with rolling function and resamples every minute to have a 00 seconds output
# return a moving average to main to continue with the writing process
def __calculate_moving_average(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    df['dates'] = df['timestamp'].astype('datetime64[s]')
    df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M:%S.%f')
    df2 = df[['dates', 'duration']]
    start_time = df2['dates'].dt.round('min').min()
    end_time = df2['dates'].dt.round('min').max()
    date_ranges = _generate_dates(end_time, start_time)
    all_df = pd.concat([df2, date_ranges])
    all_df = all_df.sort_values('dates')
    moving_average_df = all_df.rolling(str(window_size) + 'min', on='dates').mean()
    moving_average_df = moving_average_df[moving_average_df['dates'].isin(date_ranges['dates'])].fillna(
        0).drop_duplicates()
    return moving_average_df


def _generate_dates(end_time, start_time):
    return pd.DataFrame(pd.date_range(start=start_time,
                                      end=end_time + datetime.timedelta(minutes=1), freq='min'),
                        columns=['dates'])
