import pandas as pd
from typing import Callable

class EventHandler:
    """Handles events from all formats"""

    def convert_json_to_df(filename: str) -> pd.DataFrame:
        """Converts json file to a pandas Dataframe"""

        return pd.read_json(filename)


    def convert_log_to_df(filename: str) -> pd.DataFrame:
        """Converts log file to a pandas Dataframe"""

        return 'TODO'


    def convert_file_to_df(filename: str) -> Callable:
        """Receives the filename and redirected to the right function to parse the file """

        if filename.endswith('.json'):
            return EventHandler.convert_json_to_df(filename)

        elif filename.endswith('.log'):
            raise Exception('Sorry, this file format is not suported yet')

        raise Exception('Sorry, file format not suported')

    def handle_event(format: str):
        if format == 'file':
            return ''
        else:
            raise Exception('Sorry, format not suported')