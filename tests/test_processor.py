from unittest import TestCase
from src.processor.processor import process


class Test(TestCase):
    def test_with_example_data(self):
        events = [
            {
                "timestamp": "2018-12-26 18:12:19.903159",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_delivered",
                "duration": 20,
                "nr_words": 100
            },
            {
                "timestamp": "2018-12-26 18:15:19.903159",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_delivered",
                "nr_words": 30,
                "duration": 31
            },
            {
                "timestamp": "2018-12-26 18:23:19.903159",
                "translation_id": "5aa5b2f39f7254a75bb33",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "booking",
                "event_name": "translation_delivered",
                "nr_words": 100,
                "duration": 54
            }
        ]
        expected_output = [
            {
                "date": "2018-12-26 18:12:00",
                "average_delivery_time": 0
            },
            {
                "date": "2018-12-26 18:13:00",
                "average_delivery_time": 20
            },
            {
                "date": "2018-12-26 18:14:00",
                "average_delivery_time": 20
            },
            {
                "date": "2018-12-26 18:15:00",
                "average_delivery_time": 20
            },
            {
                "date": "2018-12-26 18:16:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:17:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:18:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:19:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:20:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:21:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:22:00",
                "average_delivery_time": 25.5
            },
            {
                "date": "2018-12-26 18:23:00",
                "average_delivery_time": 31
            },
            {
                "date": "2018-12-26 18:24:00",
                "average_delivery_time": 42.5
            }
        ]
        output = process(events, 10)
        self.assertEqual(expected_output, output)

    def test_when_does_not_overlap_on_windows(self):
        events = [
            {
                "timestamp": "2018-12-26 18:10:19.903159",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_delivered",
                "duration": 20,
                "nr_words": 100
            },
            {
                "timestamp": "2018-12-26 18:12:25.00000",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_delivered",
                "nr_words": 30,
                "duration": 31
            },
            {
                "timestamp": "2018-12-26 18:15:31.903159",
                "translation_id": "5aa5b2f39f7254a75bb33",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "booking",
                "event_name": "translation_delivered",
                "nr_words": 100,
                "duration": 54
            }
        ]

        expected_output = [
            {
                "date": "2018-12-26 18:10:00",
                "average_delivery_time": 0
            },
            {
                "date": "2018-12-26 18:11:00",
                "average_delivery_time": 20
            },
            {
                "date": "2018-12-26 18:12:00",
                "average_delivery_time": 20
            },
            {
                "date": "2018-12-26 18:13:00",
                "average_delivery_time": 31
            },
            {
                "date": "2018-12-26 18:14:00",
                "average_delivery_time": 31
            },
            {
                "date": "2018-12-26 18:15:00",
                "average_delivery_time": 0
            },
            {
                "date": "2018-12-26 18:16:00",
                "average_delivery_time": 54
            }
        ]
        output = process(events, 2)
        self.assertEqual(expected_output, output)
