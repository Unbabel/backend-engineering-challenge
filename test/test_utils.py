from unittest import TestCase
from src.event_reader.event_reader import read_events
from src.util.utils import *
import datetime


class TestUtils(TestCase):

    def test_get_starting_date(self):
        events = read_events("test_event.json")
        start_date = get_starting_window_datetime(events)
        self.assertEqual(start_date, datetime.datetime(
            2018, 12, 26, 18, 11, 0))

    def test_get_ending_date(self):
        events = read_events("test_event.json")
        end_date = get_ending_date_window_datetime(events)
        self.assertEqual(end_date, datetime.datetime(2018, 12, 26, 18, 24, 0))

    def test_datetime_to_string(self):
        string_date = get_string_from_datetime(
            datetime.datetime(2019, 12, 21, 0, 0, 0))
        self.assertEqual(string_date, "2019-12-21 00:00:00")

    def test_string_to_datetime(self):
        dt_date = get_datetime_from_string("2019-12-21 00:00:00.0000")
        self.assertEqual(dt_date, datetime.datetime(2019, 12, 21, 0, 0, 0, 0))
