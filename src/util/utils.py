from datetime import datetime, timedelta

STRING_FORMAT = "%y-%m-%d %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_starting_window_datetime(events_list) -> datetime:
    if events_list:
        return get_datetime_from_string(next(events_list)["timestamp"]).replace(second=0, microsecond=0)


def get_ending_date_window_datetime(event_list) -> datetime:
    if event_list:
        *_, last = event_list
        return (get_datetime_from_string(last["timestamp"]).replace(second=0, microsecond=0) + timedelta(minutes=1))


def get_datetime_from_string(date: str) -> datetime:
    return datetime.strptime(date, DATETIME_FORMAT)


def get_string_from_datetime(date: datetime) -> str:
    return datetime.strftime(date, STRING_FORMAT)


def write_to_file(period_date: datetime, average: float):
    with open("output_files/output.txt", "a+") as file:
        file.write("{{\"date\": \"{0}\", \"average_delivery_time\":{1}}},\n".format(
            get_string_from_datetime(period_date), average))
