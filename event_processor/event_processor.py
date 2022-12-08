from event_reader.event_reader import read_events

"""
    Function that takes a Json file and a window size as input and produces
    a moving average by minute

    params:
    fileName: name of the file to parse (str)
    window_size: dimensions of the window to take into consideration (int)

    output:
    a stream of events
"""


def event_processor(fileName: str, window_size: int) -> str:
    events_list = read_events(file_name=fileName)
    print(events_list)
