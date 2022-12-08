from models.event import Event
from models.avg_delivery_event import AverageDevlieryEvent
import ijson
import logging
import pdb

logging.getLogger().setLevel(logging.INFO)

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
    json_stream = ijson.items(open("example_files/" + fileName))
    event_list = (o in json_stream)
    for o in event_list:
