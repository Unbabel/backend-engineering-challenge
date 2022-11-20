import pandas as pd

class ProcessDataService:

    @staticmethod
    def group_data_by_freq(df: pd.DataFrame, freq: str = '1min') -> pd.DataFrame:
        """Pre-processes the dataframe to have buckets based on the frequency. Default is 1 minute"""

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = pd.Series(pd.to_datetime(df['timestamp'])).dt.round('T')

        df = df[['timestamp', 'duration']]

        df = df.groupby(pd.Grouper(key='timestamp', freq=freq)).mean().reset_index()

        # creates a new row at the end and shifts all durations one position
        # e.g 2018-12-26 18:23:12 should go to the bucket with min 24
        new_row = {'timestamp': df.iloc[-1]['timestamp'] +
                pd.Timedelta(minutes=1), 'duration': 0}
        df = df.append(new_row, ignore_index=True)
        df['duration'] = df['duration'].shift(1)

        df['duration'] = df['duration'].fillna(0)
        return df