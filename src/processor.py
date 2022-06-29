import datetime
import pandas as pd


def process(df, window_size) -> pd.DataFrame:
    return _calculateAvg(df, window_size)


def _calculateAvg(df, window_size) -> pd.DataFrame:
    df['dates'] = df['timestamp'].astype('datetime64[s]')
    df2 = df[['dates', 'duration']]
    start_time = df['dates'].min()
    running_time = start_time
    firstRun = True
    end_time = df['dates'].max()
    while start_time < end_time + datetime.timedelta(minutes=1):
        dummy_df = pd.DataFrame(pd.date_range(start=start_time,
                                              end=start_time + datetime.timedelta(minutes=window_size), freq='min'),
                                columns=['dates'])
        print(dummy_df)
        start_time += datetime.timedelta(minutes=window_size)
# output_frame.loc[output_frame.dates.between(df.dates), 'avg'] = df.duration
# df.resample("1m").describe.med()

#
#   2018-12-26 18:12:00, 0.0
#   2018-12-26 18:12:07, 20.0
#   2018-12-26 18:13:00, 0.0
#   2018-12-26 18:14:00, 0.0
#   2018-12-26 18:14:10, 20.0
#   2018-12-26 18:15:00, 0.0
