import argparse
import os


class Reader():
    def __init__(self, filepath, window_size):
        self.filepath = filepath
        self.window_size = window_size
    
    def read_input(self):
        full_path = os.path.abspath(self.filepath)
        window_size = self.window_size

        if not self.__file_exists(full_path):
            return False

        if not self.__is_valid_window_size(self.window_size):
            return False

        return {"file": full_path, "window_size": window_size}

    def __file_exists(self, fullpath):
        is_file = os.path.isfile(fullpath)
        if not is_file:
            return False
        
        return True

    def __is_valid_window_size(self, window_size):
        try:
            int(window_size)
        except ValueError:
            return False

        is_positive_window = self.__is_window_positive(window_size)
        is_window_integer = self.__is_window_integer(window_size)

        return is_positive_window and is_window_integer

    def __is_window_positive(self, window_size):
        return window_size > 0

    def __is_window_integer(self, window_size):
        return isinstance(window_size, int)
