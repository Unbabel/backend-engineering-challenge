from datetime import datetime as dt


def processEvents(df):
    _calculateAvg(df, 10, )


def _calculateAvg(events, windowSize, initialDate):
    picked_records = events[(events['timestamp'] < '2022-6-28 14:20:5')]
    avg = picked_records['duration'].mean()
    print(avg)
