
"""
Datetime operations
"""

from .settings import (
    DEFAULT_TIME_FORMAT,
    DEFAULT_OUTPUT_TIME_FORMAT,
    TIME_FORMAT_WITHOUT_MICROSECONDS
)
from datetime import datetime, timedelta


def get_datetime_from_string(datetime_string, time_format=DEFAULT_TIME_FORMAT):
    """
    Returns datetime object representations of string.
    """

    try:
        timestamp = datetime.strptime(datetime_string, time_format)
    except ValueError:
        timestamp = datetime.strptime(
            datetime_string, TIME_FORMAT_WITHOUT_MICROSECONDS
        )

    return timestamp


def get_string_from_datetime(timestamp, output_time_format=DEFAULT_OUTPUT_TIME_FORMAT):
    """
    Returns string representation of timestamp.
    """

    return timestamp.strftime(output_time_format)


def get_rounded_off_datetime(datetime_object):
    """
    Returns rounded off datetime object.
    Example: 2018-12-26 18:11:08.509655 --> 2018-12-26 18:11:00
    """

    return datetime_object.replace(second=0, microsecond=0)


def get_difference_in_number_of_minutes(end, start):
    """
    Returns number of minutes lapsed between two timestamps.
    """

    time_difference = end - start
    number_of_minutes = time_difference.total_seconds()/60

    return number_of_minutes


def add_minutes(timestamp, minutes):
    """
    Return `minutes` moved forward timestamp.
    """

    return (timestamp + timedelta(minutes=int(minutes)))


def subtract_minutes(timestamp, minutes):
    """
    Return `minutes` moved backward timestamp.
    """

    return (timestamp - timedelta(minutes=int(minutes)))
