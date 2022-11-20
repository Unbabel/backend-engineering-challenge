import pandas as pd
import os

from services.moving_average_service import MovingAverageService

def test_simple_moving_average():
    """Should return a dataframe with a new column ['sma'] with the simple moving
    average for the events"""

    df_path = os.path.join(os.path.dirname(__file__), '../data/pre_processed_df.csv')
    df = pd.read_csv(df_path)

    result = MovingAverageService.simple_moving_average(df, 10)

    expected_result = [0, 20, 20, 20, 20, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 31, 42.5]

    for index, row in result.iterrows():
        assert row['sma'] == expected_result[index]


def test_calc_index_timestamps_1():
    """Should return the indexes of the window based on the current index and window size"""

    start, end = MovingAverageService.calc_index_timestamps(4, 10)
    assert start == 4
    assert end == 0

def test_calc_index_timestamps_2():
    """Should return the indexes of the window based on the current index and window size"""

    start, end = MovingAverageService.calc_index_timestamps(14, 10)
    assert start == 14
    assert end == 4

def test_calc_index_timestamps_3():
    """Should return the indexes of the window based on the current index and window size"""

    start, end = MovingAverageService.calc_index_timestamps(0, 10)
    assert start == 0
    assert end == 0