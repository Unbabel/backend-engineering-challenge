import pandas as pd
import os


from handlers.event_handler import EventHandler
from services.process_data_service import ProcessDataService

def test_group_data_by_freq():
    """Should pre-process a dataframe to have buckets based on the frequency"""

    json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/input.json')
    df = EventHandler.convert_json_to_df(json_path)
    result = ProcessDataService.group_data_by_freq(df)
    assert len(result) == 14
    assert result.columns.values.tolist() == ['timestamp', 'duration']
    assert result.duration.values.tolist() == [0.0, 20.0, 0.0, 0.0, 0.0, 31.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 54.0]
