from datetime import datetime, timedelta

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_average(events):
    average = 0
    total_duration_sum = 0
    total_count = 0

    if not len(events):
        return average

    for key in events.keys():
        total_duration_sum += events[key]['duration']
        total_count += events[key]['count']

    average = total_duration_sum / total_count

    return format_number(average)


def format_number(number):
    if number % 1 == 0:
        return int(number)
    return number


def get_datetime_from_string(datetime_string, time_format=TIMESTAMP_FORMAT):
    try:
        timestamp = datetime.strptime(datetime_string, time_format)
    except ValueError:
        timestamp = datetime.strptime(
            datetime_string, DATETIME_FORMAT
        )

    return timestamp


def get_string_from_datetime(timestamp, output_time_format=DATETIME_FORMAT):
    return timestamp.strftime(output_time_format)


def get_rounded_off_datetime(datetime_object):
    return datetime_object.replace(second=0, microsecond=0)


def get_difference_in_number_of_minutes(end, start):
    time_difference = end - start
    number_of_minutes = time_difference.total_seconds() / 60

    return number_of_minutes


def add_minutes(timestamp, minutes):
    return timestamp + timedelta(minutes=int(minutes))


def subtract_minutes(timestamp, minutes):
    return timestamp - timedelta(minutes=int(minutes))
