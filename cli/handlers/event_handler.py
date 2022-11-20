import pandas as pd
from typing import Callable

from schemas.translation_event_schema import TranslationEventSchema
class EventHandler:
    """Handles events from all formats"""

    def convert_json_to_df(filename: str) -> pd.DataFrame:
        """Converts json file to a pandas Dataframe"""

        try:
            df = pd.read_json(filename)
        except:
            raise ValueError('Could not convert file into Dataframe')

        if df.columns.values.tolist() != TranslationEventSchema.values:
            raise ValueError('Dataframe does not have the right schema')

        return df

    def convert_file_to_df(filename: str) -> Callable:
        """Receives the filename and redirected to the right function to parse the file """

        if filename.endswith('.json'):
            return EventHandler.convert_json_to_df(filename)

        elif filename.endswith('.log'):
            raise Exception('Sorry, this file format is not suported yet')

        raise Exception('Sorry, file format not suported')
