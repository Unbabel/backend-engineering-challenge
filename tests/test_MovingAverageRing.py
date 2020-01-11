import unittest

from enki.MovingAverageRing import MovingAverageRing


class TestMovingAverageRing(unittest.TestCase):
    def test_window_0(self):
        with self.assertRaises(ValueError):
            MovingAverageRing(0)

    def test_window_1(self):
        ma = MovingAverageRing(1)

        self.assertEqual(ma.get(), 0)

        ma.append(20)
        self.assertEqual(ma.get(), 20)

        ma.append(-20)
        self.assertEqual(ma.get(), -20)

    def test_window_2(self):
        ma = MovingAverageRing(2)

        self.assertEqual(ma.get(), 0)

        ma.append(20)
        self.assertEqual(ma.get(), 20)

        ma.append(-20)
        self.assertEqual(ma.get(), 0)

        ma.append(10)
        self.assertEqual(ma.get(), -5)
        ma.append(0)
        self.assertEqual(ma.get(), 5)

        ma.append(4)
        self.assertEqual(ma.get(), 2)

        ma.append(-4)
        self.assertEqual(ma.get(), 0)

    def test_populated_average(self):
        ma = MovingAverageRing(3)

        self.assertEqual(ma.get_populated_average(), 0)

        ma.append(10)
        self.assertEqual(ma.get(), 10)
        self.assertEqual(ma.get_populated_average(), 10)

        ma.append(None)
        self.assertEqual(ma.get(), 5)
        self.assertEqual(ma.get_populated_average(), 10)

        ma.append(50)
        self.assertEqual(ma.get(), 20)
        self.assertEqual(ma.get_populated_average(), 30)

    def test_given_example(self):
        ma = MovingAverageRing(10)

        self.assertEqual(ma.get_populated_average(), 0)

        ma.append(20)  # 12
        self.assertEqual(ma.get_populated_average(), 20)

        ma.append(None)  # 13
        self.assertEqual(ma.get_populated_average(), 20)

        ma.append(None)  # 14
        self.assertEqual(ma.get_populated_average(), 20)

        ma.append(None)  # 15
        self.assertEqual(ma.get_populated_average(), 20)

        ma.append(31)  # 16
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 17
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 18
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 19
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 20
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 21
        self.assertEqual(ma.get_populated_average(), 25.5)

        ma.append(None)  # 22
        self.assertEqual(ma.get_populated_average(), 31)

        ma.append(None)  # 23
        self.assertEqual(ma.get_populated_average(), 31)

        ma.append(54)  # 24
        self.assertEqual(ma.get_populated_average(), 42.5)

        self.assertEqual(ma.get(), 8.5)
