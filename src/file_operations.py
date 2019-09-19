"""
Handles file operations
"""


from .settings import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE


def get_file_stream_to_read(filename=DEFAULT_INPUT_FILE):
    """
    Returns a file object reference of filename.
    """

    return open(filename)


def get_file_stream_to_write(filename=DEFAULT_OUTPUT_FILE):
    """
    """

    return open(filename, 'w+')


def close_file_stream(file_stream):
    """
    Closes file reference
    """

    file_stream.close()
