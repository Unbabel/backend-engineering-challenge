import pandas as pd

class MovingAverageService:
    """Class to create movie clips"""
    
    def calc_index_timestamps(current_index: int, window_size: int):
        """Calculates the start and end index based on the window size"""

        # case when start is smaller than the window size and would overflow
        if current_index-window_size <= 0:
            return current_index, 0

        return current_index, current_index-window_size


    def simple_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
        """Calculates a simple moving average for events"""
        result = []

        for index, row in df.iterrows():
            end_index, start_index = MovingAverageService.calc_index_timestamps(index, window)
            temp_df = df.iloc[start_index:end_index+1]

            # only timestamps where an event occured are used to calculate sma
            temp_df = temp_df.loc[temp_df['duration'] > 0]
            s = temp_df['duration'].values.tolist()
            if len(s) > 0:
                result.append(sum(s)/len(s))
            else:
                result.append(0)

        df['sma'] = result
        return df

