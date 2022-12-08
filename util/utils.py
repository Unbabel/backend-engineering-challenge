from datetime import datetime
from models.event import Event

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
STRING_FORMAT =


def timestamp_to_datetime(event, time_format=TIMESTAMP_FORMAT) -> Event:
    event["timestamp"] = datetime.strptime(event["timestamp"], time_format)
    return event
