import unittest
import json
from datetime import datetime
from unbabel_cli import parse_event, moving_average

class TestMovingAverages(unittest.TestCase):
    def setUp(self):
        self.events = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 18:15:19.903159", "duration": 31},
            {"timestamp": "2018-12-26 18:23:19.903159", "duration": 54}
        ]
        self.parsed_events = [
            {"timestamp": datetime(2018, 12, 26, 18, 11, 8, 509654), "duration": 20},
            {"timestamp": datetime(2018, 12, 26, 18, 15, 19, 903159), "duration": 31},
            {"timestamp": datetime(2018, 12, 26, 18, 23, 19, 903159), "duration": 54}
        ]

    def test_parse_event(self):
        parsed = [parse_event(event) for event in self.events]
        self.assertEqual(parsed, self.parsed_events)

    def test_moving_average(self):
        results = moving_average(self.parsed_events, 10)
        expected_results = [
            {"date": "2018-12-26 18:11:00", "average_delivery_time": 0},
            {"date": "2018-12-26 18:12:00", "average_delivery_time": 20},
            {"date": "2018-12-26 18:13:00", "average_delivery_time": 20},
            {"date": "2018-12-26 18:14:00", "average_delivery_time": 20},
            {"date": "2018-12-26 18:15:00", "average_delivery_time": 20},
            {"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5},
            {"date": "2018-12-26 18:22:00", "average_delivery_time": 31},
            {"date": "2018-12-26 18:23:00", "average_delivery_time": 31},
            {"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
        ]
        self.assertEqual(results, expected_results)

    # Add other tests here if needed

if __name__ == '__main__':
    unittest.main()
