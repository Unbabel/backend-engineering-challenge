from lib.event_processor.event_processor import EventProcessor
from lib.event_reader.event_reader import EventReader
import unittest
import os

class EventProcessorTest(unittest.TestCase):
    """Event Processor unit test."""

    def test_event_processor_with_a_valid_file(self):
        filepath = os.getcwd() + "/tests/support/events_default.json"
        processor = EventProcessor(filepath, EventReader())
        self.assertEqual(len(processor.get_events_list()), 3)

    def test_order_events_to_list_with_valid_timestamp(self):
        filepath = os.getcwd() + "/tests/support/events_default.json"
        processor = EventProcessor(filepath, EventReader())
        event_list = processor.order_list()

        first_element = event_list[0]
        last_element = event_list[-1]

        self.assertEqual(first_element.translation_id, "5aa5b2f39f7254a75aa5")
        self.assertEqual(last_element.translation_id, "5aa5b2f39f7254a75bb33")
    
    def test_calculate_average_datetime_with_two_events(self):
        filepath = os.getcwd() + "/tests/support/two_events.json"
        processor = EventProcessor(filepath, EventReader())
        
        output = processor.calculate_date_range(10)
        first_output = output[0]
        second_output = output[1]
        third_output = output[2]
        fourth_output = output[3]
        
        self.assertEqual(len(output), 4)
        self.assertEqual(first_output.get('average_delivery_time'), 0)
        self.assertEqual(second_output.get('average_delivery_time'), 20)
        self.assertEqual(third_output.get('average_delivery_time'), 20)
        self.assertEqual(fourth_output.get('average_delivery_time'), 25.5)

    def test_calculate_average_datetime_with_different_days(self):
        filepath = os.getcwd() + "/tests/support/events_with_diff_dates.json"
        processor = EventProcessor(filepath, EventReader())
        
        output = processor.calculate_date_range(10)
        first_output = output[0]
        last_output = output[-1]

        self.assertEqual(first_output.get('date'), "2018-12-26 18:11:00")
        self.assertEqual(last_output.get('date'), "2018-12-27 18:16:00")


if __name__ == '__main__':
    unittest.main()
    