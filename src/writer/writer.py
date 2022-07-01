import pandas as pd


def write(output_frame: pd.DataFrame):
    output_frame = output_frame.rename(columns={'dates': 'date', 'duration': 'average_delivered_time'})
    output_frame['date'] = pd.to_datetime(output_frame['date'], format='%Y-%m-%d %H:%M:%S').dt.strftime(
        '%Y-%m-%d %H:%M:%S')
    print(output_frame)
    output_frame.to_json('files/output.json', orient='records', date_format='iso', date_unit='s', lines=True)
