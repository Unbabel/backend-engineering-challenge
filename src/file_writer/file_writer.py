import datetime
from src.util.utils import get_string_from_datetime


def write_to_file(period_date: datetime, average: float):
    with open("output_files/output.txt", "a+") as file:
        file.write("{{\"date\": \"{0}\", \"average_delivery_time\":{1}}},\n".format(
            get_string_from_datetime(period_date), average))
