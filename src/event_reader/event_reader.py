from typing import List
import ijson
from src.models.event import Event
import pydantic

"""
    Function that from a json stream creates a list of Event objects

    params:
        file_name: file name
     output:
        event_list: List of Event objects
"""


def read_events(file_name: str) -> List[Event]:
    event_list = []
    event_stream = ijson.items(open("example_files/" + file_name), "item")
    for item in event_stream:
        try:
            new_event = Event(**item)
        except pydantic.ValidationError as err:
            print(err)
        event_list.append(new_event)
    return event_list
