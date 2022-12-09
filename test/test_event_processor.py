from unittest import TestCase
from src.event_processor.event_processor import _calculate_average


class TestEventProcessor(TestCase):

    def test_calculate_average_with_nonzero_counter(self):
        counter = 12
        total_duration = 300
        self.assertEqual(_calculate_average(total_duration, counter), 25.0)

    def test_calculate_average_with_zero_counter(self):
        counter = 0
        total_duration = 300
        self.assertEqual(_calculate_average(total_duration, counter), 0.0)
