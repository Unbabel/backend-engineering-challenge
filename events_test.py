import unittest
from unittest.mock import patch
from main import calculate_moving_average, save_to_file
import json 
class EventsTests(unittest.TestCase):
    @patch('builtins.print')  # Mock the print function to capture output
    def test_calculate_moving_average(self, mock_print):
        # Prepare test data
        input_file = 'test_input.json'
        window_size = 5

        # Mocking events for testing
        test_events = [
            {"timestamp": "2022-01-01 12:00:00.000", "duration": 10},
            {"timestamp": "2022-01-01 12:05:00.000", "duration": 20},
            {"timestamp": "2022-01-01 12:07:00.000", "duration": 30},
        ]

        with patch('builtins.open', create=True) as mock_open:
            # Mocking the file read to return test_events
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(test_events)

            # Run the function to test
            calculate_moving_average(input_file, window_size)

        # Assertions based on the expected output
        mock_print.assert_called_with({"date": "2022-01-01 12:00:00", "average_delivery_time": 10.0})
        mock_print.assert_called_with({"date": "2022-01-01 12:05:00", "average_delivery_time": 20.0})
        mock_print.assert_called_with({"date": "2022-01-01 12:07:00", "average_delivery_time": 30.0})


    def test_save_to_file(self):
        # Test data
        average_time = [{"date": "2022-01-01 12:00:00", "average_delivery_time": 15.0}]

        with patch('builtins.print') as mock_print:
            # Run the function to test
            save_to_file(average_time)

        # Assertions based on the expected output
        mock_print.assert_called_with({"date": "2022-01-01 12:00:00", "average_delivery_time": 15.0})

if __name__ == '__main__':
    unittest.main()
