from datetime import datetime, timedelta
from typing import List

from src.models.event import Event


def sort_by_datetime(event_list):
    event_list.sort(key=lambda x: x.timestamp)


def get_starting_window_datetime(events_list: List[Event]) -> datetime:
    if events_list:
        return events_list[0].timestamp


def get_ending_window_datetime(start_date: datetime, window_size: int) -> datetime:
    return start_date + timedelta(minutes=window_size)
