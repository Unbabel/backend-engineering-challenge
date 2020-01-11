import unittest

from enki.PerMinuteMovingAverageCalculator import PerMinuteMovingAverageCalculator


class TestPerMinuteMovingAverageCalculator(unittest.TestCase):
    emitted: list

    def setUp(self):
        self.emitted = []

    def tearDown(self):
        self.emitted = []

    def sink(self, data: dict):
        self.emitted.append(data)

    def get_bucket_key(self, data):
        # Minute part, zero-out seconds.
        return "%s:00" % data["timestamp"][:16]

    def get_calc(self, window):
        return PerMinuteMovingAverageCalculator(
            self.sink, window, self.get_bucket_key, lambda x: x["duration"], "date", "average_delivery_time")

    def test_window_0(self):
        with self.assertRaises(ValueError):
            self.get_calc(0)

    def test_window_1_1(self):
        calc = self.get_calc(1)
        data = [{"timestamp": "2018-12-26 18:11:08.509654", "duration": 20}]
        for d in data:
            calc.consume(d)

        self.assertEqual(0, len(self.emitted))

        calc.end()

        self.assertEqual(self.emitted, [
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
        ])

    def test_window_1_4(self):
        calc = self.get_calc(1)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40},
            {"timestamp": "2018-12-26 18:13:09.509654", "duration": 50},
            {"timestamp": "2018-12-26 18:15:09.509654", "duration": 60},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(5, len(self.emitted))

        calc.end()

        self.assertEqual([
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:13:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:14:00', 'average_delivery_time': 90.0},
            {'date': '2018-12-26 18:15:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:16:00', 'average_delivery_time': 60.0},
        ], self.emitted)

    def test_window_2_2(self):
        calc = self.get_calc(2)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(3, len(self.emitted))

        calc.end()

        self.assertEqual([
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:13:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:14:00', 'average_delivery_time': 40.0},
        ], self.emitted)

    def test_window_3_2(self):
        calc = self.get_calc(3)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(3, len(self.emitted))

        calc.end()

        self.assertEqual([
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:13:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:14:00', 'average_delivery_time': 30.0},
        ], self.emitted)

    def test_window_10_4(self):
        calc = self.get_calc(10)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40},
            {"timestamp": "2018-12-26 18:14:08.509654", "duration": 10},
            {"timestamp": "2018-12-26 18:14:08.509654", "duration": 14},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(4, len(self.emitted))

        calc.end()

        self.assertEqual([
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:13:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:14:00', 'average_delivery_time': 30.0},
            {'date': '2018-12-26 18:15:00', 'average_delivery_time': 28.0},
        ], self.emitted)

    def test_single(self):
        calc = self.get_calc(10)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en",
                "target_language": "fr", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 30, "duration": 20},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(0, len(self.emitted))

        calc.end()

        self.assertEqual([
            {"date": "2018-12-26 18:11:00", "average_delivery_time": 0},
            {"date": "2018-12-26 18:12:00", "average_delivery_time": 20},
        ], self.emitted)

    def test_example(self):
        calc = self.get_calc(10)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en",
                "target_language": "fr", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 30, "duration": 20},
            {"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4", "source_language": "en",
                "target_language": "fr", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 30, "duration": 31},
            {"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb33", "source_language": "en",
                "target_language": "fr", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 100, "duration": 54},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(13, len(self.emitted))

        calc.end()

        self.assertEqual([
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
            {"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5},
        ], self.emitted)

    def test_window_10_multi(self):
        calc = self.get_calc(10)
        data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20},
            {"timestamp": "2018-12-26 19:13:08.509654", "duration": 40},
        ]
        for d in data:
            calc.consume(d)

        self.assertEqual(63, len(self.emitted))

        calc.end()

        self.assertEqual([
            {'date': '2018-12-26 18:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:12:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:13:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:14:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:15:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:16:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:17:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:18:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:19:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:20:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:21:00', 'average_delivery_time': 20.0},
            {'date': '2018-12-26 18:22:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:23:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:24:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:25:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:26:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:27:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:28:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:29:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:30:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:31:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:32:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:33:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:34:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:35:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:36:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:37:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:38:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:39:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:40:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:41:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:42:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:43:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:44:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:45:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:46:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:47:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:48:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:49:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:50:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:51:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:52:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:53:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:54:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:55:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:56:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:57:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:58:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 18:59:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:00:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:01:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:02:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:03:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:04:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:05:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:06:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:07:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:08:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:09:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:10:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:11:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:12:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:13:00', 'average_delivery_time': 0},
            {'date': '2018-12-26 19:14:00', 'average_delivery_time': 40.0}
        ], self.emitted)
