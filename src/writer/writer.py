import pandas as pd


def write(output_frame):
    print(output_frame)
    output_frame.to_json('files/output.json', orient='records', date_format='iso', lines=True)
