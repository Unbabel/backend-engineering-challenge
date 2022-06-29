from datetime import datetime
import pandas as pd

date_format = '%Y-%m-%d %H:%M:%S.%f'


def _calculateMovingAvg(events, window_size):
    res = sorted(events, key=lambda x: datetime.strptime(x['timestamp'], date_format))
    start_tms = res[0]['timestamp']
    running_tms = res[0]['timestamp']
    end_tms = res[len(events) - 1]['timestamp']
    left_side = 0
    right_side = 0
    dfRangeTime = pd.date_range(start_tms, end_tms, freq="1min")
    while left_side < len(dfRangeTime):
        while(start_tms + pd.to_timedelta())

def process(events, window_size):
    _calculateMovingAvg(events, window_size)
    return None
