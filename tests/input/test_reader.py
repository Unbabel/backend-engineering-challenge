from lib.input.reader import Reader
import unittest
import os

class ReaderTest(unittest.TestCase):
    """Reader unit test."""

    def test_read_input_with_negative_window_size(self):
        reader = Reader("tests/support/events_default.json", -20)
        self.assertFalse(reader.read_input())

    def test_read_input_with_string_window_size(self):
        reader = Reader("tests/support/events_default.json", "abc")
        self.assertFalse(reader.read_input())

    def test_read_input_with_not_integer_number_window_size(self):
        reader = Reader("tests/support/events_default.json", 20.5)
        self.assertFalse(reader.read_input())
        
    def test_read_input_with_invalid_file(self):
        reader = Reader("tests/support/events404.json", 20)
        self.assertFalse(reader.read_input())

    def test_read_input_with_valid_data(self):
        path = "tests/support/events_default.json"
        reader = Reader(path, 20)
        input_data = reader.read_input()
    
        self.assertEqual(
            {
                "file": os.path.abspath(path),
                "window_size": 20
            },
            input_data
        )