from datetime import datetime, timedelta
from typing import List

from src.models.event import Event
from src.models.output_event import OutputEvent
import json

STRING_FORMAT = "%y-%m-%d %H:%M:%S"


def sort_by_datetime(event_list):
    event_list.sort(key=lambda x: x.timestamp)


def get_starting_window_datetime(events_list: List[Event]) -> datetime:
    if events_list:
        return events_list[0].timestamp.replace(second=0, microsecond=0)


def get_ending_window_datetime(start_date: datetime, window_size: int) -> datetime:
    return start_date + timedelta(minutes=window_size)


def write_to_file(period_date: datetime, average: float):
    with open("output_files/" + datetime.now().strftime("%m-%d-%YT%H:%M:%S") + ".txt", "a+") as file:
        file.write(json.dumps(OutputEvent(date=period_date.strftime(STRING_FORMAT),
                   average_delivery_time=average).__dict__)+"\n")
