from datetime import datetime

date_format = '%Y-%m-%d %H:%M:%S.%f'


def _calculateMovingAvg(events, window_size):
    res = sorted(events, key=lambda x: datetime.strptime(x['timestamp'], date_format))
    start_tms = res[0]['timestamp']
    running_tms = res[0]['timestamp']
    end_tms = res[len(events) - 1]['timestamp']
    while running_tms < end_tms:



def process(events, window_size):
    _calculateMovingAvg(events, window_size)
    return None
