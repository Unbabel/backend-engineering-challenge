import unittest
from translate import data_processing
from translate.utils import read_file

class TestOutput(unittest.TestCase):
    def test_with_window_size_10(self):
        data = read_file("data.json")
        expected_output = read_file("testfiles/window_size10.json")
        output = data_processing(data, 10)
        self.assertEqual(output, expected_output)

    def test_with_window_size_9(self):
        data = read_file("data.json")
        expected_output = read_file("testfiles/window_size9.json")
        output = data_processing(data, 9)
        self.assertEqual(output, expected_output)

    def test_with_window_size_8(self):
        data = read_file("data.json")
        expected_output = read_file("testfiles/window_size8.json")
        output = data_processing(data, 8)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()