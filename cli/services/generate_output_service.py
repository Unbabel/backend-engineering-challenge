import pandas as pd

class GenerateOutputService:

    @staticmethod
    def create_json_file(df: pd.DataFrame, output_file: str ='./output.json', orient: str ='records'):
        """Creates a json output"""

        df.rename(columns={'timestamp': 'date',
                'sma': 'average_delivery_time'}, inplace=True)
        df['date'] = df['date'].astype(str)
        df[['date', 'average_delivery_time']].to_json(output_file, orient=orient)