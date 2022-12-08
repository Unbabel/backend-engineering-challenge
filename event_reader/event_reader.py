from typing import List
import ijson
from models.event import Event
from util.utils import timestamp_to_datetime
import pydantic


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
