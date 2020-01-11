import unittest

from enki.MovingAverageCalculator import MovingAverageCalculator


class TestMovingAverageCalculator(unittest.TestCase):
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
        return MovingAverageCalculator(
            self.sink, window, self.get_bucket_key, lambda x: x["duration"], "date", "average_delivery_time")

    def test_window_0(self):
        with self.assertRaises(ValueError):
            self.get_calc(0)

    def test_window_1(self):
        calc = self.get_calc(1)
        calc.consume(
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20})

        self.assertEqual(len(self.emitted), 0)

        calc.end()

        self.assertEqual(len(self.emitted), 1)
        self.assertEqual(self.emitted[0]["average_delivery_time"], 20)

    def test_window_1_2(self):
        calc = self.get_calc(1)
        calc.consume(
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20})
        calc.consume(
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40})

        self.assertEqual(len(self.emitted), 1)

        calc.end()

        self.assertEqual(len(self.emitted), 2)
        self.assertEqual(self.emitted[0]["average_delivery_time"], 20)
        self.assertEqual(self.emitted[1]["average_delivery_time"], 40)

    def test_window_2_2(self):
        calc = self.get_calc(2)
        calc.consume(
            {"timestamp": "2018-12-26 18:11:08.509654", "duration": 20})
        calc.consume(
            {"timestamp": "2018-12-26 18:13:08.509654", "duration": 40})

        self.assertEqual(len(self.emitted), 1)

        calc.end()

        self.assertEqual(len(self.emitted), 2)
        self.assertEqual(self.emitted[0]["average_delivery_time"], 20)
        self.assertEqual(self.emitted[1]["average_delivery_time"], 30)
