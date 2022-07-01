import pandas as pd


def write(output_frame: pd.DataFrame):
    output_frame = output_frame.rename(columns={'dates': 'date', 'duration': 'average_delivered_time'})
    output_frame.to_json('files/output.json', orient='records', date_format='iso', lines=True)
