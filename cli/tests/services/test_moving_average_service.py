import pandas as pd
import os

from services.moving_average_service import MovingAverageService

def test_simple_moving_average_1():
    """Should return a dataframe with a new column ['sma'] with the simple moving
    average for the events"""

    df_path = os.path.join(os.path.dirname(__file__), '../data/pre_processed_df.csv')
    df = pd.read_csv(df_path)

    result = MovingAverageService.simple_moving_average(df, 10)

    expected_result = [0, 20, 20, 20, 20, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 31, 42.5]

    for index, row in result.iterrows():
        assert row['sma'] == expected_result[index]

