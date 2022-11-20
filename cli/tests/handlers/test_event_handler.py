import pandas as pd
import os
import pytest

from handlers.event_handler import EventHandler
from schemas.translation_event_schema import TranslationEventSchema

def test_convert_json_to_df_1():
    """Should read a json file and return a Dataframe"""

    json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/input.json')
    result = EventHandler.convert_json_to_df(json_path)
    assert len(result) == 3
    assert result.columns.values.tolist() == TranslationEventSchema.values

def test_convert_json_to_df_2():
    """Should raise an error with invalid filename"""

    with pytest.raises(Exception) as e_info:

        json_path = os.path.join(os.path.dirname(__file__), '/fake/path/input.json')
        result = EventHandler.convert_json_to_df(json_path)

    assert 'Could not convert file into Dataframe' in str(e_info)

def test_convert_json_to_df_3():
    """Should raise an error with invalid schema"""

    with pytest.raises(Exception) as e_info:

        json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/invalid_input.json')
        result = EventHandler.convert_json_to_df(json_path)

    assert 'Dataframe does not have the right schema' in str(e_info)
    
def test_convert_file_to_df_1():
    """Should route the file to the right parser based on the extention of the file"""

    json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/input.json')
    result = EventHandler.convert_file_to_df(json_path)
    assert len(result) == 3
    assert result.columns.values.tolist() == TranslationEventSchema.values

def test_convert_file_to_df_2():
    """Should raise an error with log format not suported yet"""
    
    with pytest.raises(Exception) as e_info:

        json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/invalid_input.log')
        result = EventHandler.convert_file_to_df(json_path)

    assert 'Sorry, this file format is not suported yet' in str(e_info)

def test_convert_file_to_df_3():
    """Should raise an error with file format not suported"""

    with pytest.raises(Exception) as e_info:

        json_path = os.path.join(os.path.dirname(__file__), '../../../data/inputs/invalid_input.txt')
        result = EventHandler.convert_file_to_df(json_path)

    assert 'Sorry, file format not suported' in str(e_info)