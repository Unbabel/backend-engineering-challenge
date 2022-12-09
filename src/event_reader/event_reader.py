import ijson

"""
    Function that from a json stream creates a list of Event objects

    params:
        file_name: file name
     output:
        event_list: iterator object representing the json stream
"""


def read_events(file_name: str):
    event_stream = ijson.items(open("example_files/" + file_name), "item")
    events = (event for event in event_stream)
    return events
