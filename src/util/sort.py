from datetime import datetime

date_format = '%Y-%m-%d %H:%M:%S.%f'


def sortEventList(events: list):
    return sorted(events, key=lambda x: datetime.strptime(x['timestamp'], date_format))
