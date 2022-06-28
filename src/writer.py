import pandas as pd


def write(out_frame):
    output = pd.DataFrame(out_frame)
    output.to_json('files/output.json')
