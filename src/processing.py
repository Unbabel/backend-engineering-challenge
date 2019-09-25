from typing import List, Dict, Text, Any
from pandas import DataFrame
from datetime import datetime, timedelta
import numpy as np


def moving_averages(events: DataFrame, window_size: int) -> List[Dict[Text, Any]]:
    """Return moving average of durations from an events dataframe."""

    timestamps = events.timestamp.values

    first_timestamp = _round_to_minute(timestamps[0], upwards=False)
    last_timestamp = _round_to_minute(timestamps[-1], upwards=True)

    delta = last_timestamp - first_timestamp
    num_windows = int(delta.total_seconds() // 60) + 1

    averages = []

    for i in range(num_windows):

        start = first_timestamp + timedelta(minutes=i - window_size)
        end = first_timestamp + timedelta(minutes=i)
        window = events[end > events.timestamp][events.timestamp > start]

        window.fillna(0)

        if len(window) == 0:
            avg = 0
        else:
            avg = np.mean(window.duration)

        averages.append({"date": end, "average_delivery_time": avg})

    return averages


def _round_to_minute(timestamp: datetime, upwards: bool) -> datetime:
    """Rounds a given timestamp to the nearest minute."""

    minute = timestamp.minute

    if upwards is True and timestamp.second > 0:
        minute += 1

    return datetime(
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=minute,
    )
