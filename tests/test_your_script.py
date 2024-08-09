import pytest
from unittest.mock import mock_open, patch
from unbabel_cli import calculate_moving_average

def test_calculate_moving_average(capsys):
    # Sample input data
    input_data = """{"timestamp": "2018-12-26 18:11:08.509654", "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159", "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159", "duration": 54}
"""

    # Expected output based on the actual function behavior
    expected_output = [
        '{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}',
        '{"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0}',
        '{"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0}',
        '{"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0}',
        '{"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0}',
        '{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}',
        '{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}',
        '{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}',
        '{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}',
        '{"date": "2018-12-26 18:25:00", "average_delivery_time": 42.5}',
        '{"date": "2018-12-26 18:26:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:27:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:28:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:29:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:30:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:31:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:32:00", "average_delivery_time": 54.0}',
        '{"date": "2018-12-26 18:33:00", "average_delivery_time": 54.0}',
    ]

    # Use mock_open to simulate file reading
    with patch("builtins.open", mock_open(read_data=input_data)):
        # Call the function with a mock file path and window size
        calculate_moving_average("mock_file_path", 10)

        # Capture the output
        captured = capsys.readouterr()

        # Split the output into lines and compare with expected output
        actual_output = [line.strip() for line in captured.out.splitlines()]
        assert actual_output == expected_output
