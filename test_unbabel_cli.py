import unittest
from datetime import datetime, timedelta
from unbabel_cli import UnbabelCLI


class TestUnbabelCLI(unittest.TestCase):

    def setUp(self):
        self._cli = UnbabelCLI('events.json', 13, 'data.json')

    def test_is_valid_event1(self):
        self.assertFalse(self._cli._is_valid_event({
            "event_name": "Unknown",
            "name": "xyz",
            "language": "English"
        }))

    def test_is_valid_event2(self):
        self.assertTrue(self._cli._is_valid_event({
            "timestamp": "2018-12-26 18:12:19.903159",
            "translation_id": "5aa5b2f39f7254a75aa4",
            "source_language": "en",
            "target_language": "fr",
            "client_name": "easyjet",
            "event_name": "translation_delivered",
            "duration": 20,
            "nr_words": 100
        }))

    def test_is_valid_event3(self):
        self.assertFalse(self._cli._is_valid_event({
            "timestamp": "2018-12-26 18:12:19.903159",
            "translation_id": "5aa5b2f39f7254a75aa4",
            "source_language": "en",
            "target_language": "fr",
            "client_name": "easyjet",
            "event_name": "translation_delivered",
            "nr_words": 100
        }))

    def test_validate_arguments1(self):
        test_obj = UnbabelCLI("events.json", -10)
        with self.assertRaises(ValueError):
            test_obj._validate_args()

    def test_validate_arguments2(self):
        test_obj = UnbabelCLI("evnts.json", 10)
        with self.assertRaises(ValueError):
            test_obj._validate_args()

    def test_get_most_recent_event(self):
        self.assertDictEqual(self._cli._get_next_recent_event().__next__(),
                             {
                                 'timestamp': '2018-12-26 18:23:00.000000',
                                 'translation_id': '5aa5b2f39f7254a75bb33',
                                 'source_language': 'en',
                                 'target_language': 'fr',
                                 'client_name': 'booking',
                                 'event_name': 'translation_delivered',
                                 'nr_words': 200,
                                 'duration': 94
                             })

    def test_parse_and_process_events(self):
        self._cli._parse_and_process_events()
        self.assertIsNotNone(self._cli._date_timestamp_durations_map)
        self.assertIsNotNone(self._cli._highest_window_timestamp)
        self.assertIsNotNone(self._cli._lowest_window_timestamp)
        avg_time = self._cli.get_average_delivery_time(datetime.strptime("2018-12-26 18:13:00", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(avg_time, 15)
        avg_time = self._cli.get_average_delivery_time(datetime.strptime("2018-12-26 18:22:00", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(avg_time, 20.3)


    def tearDown(self):
        delattr(self, "_cli")


if __name__ == "__main__":
    unittest.main()