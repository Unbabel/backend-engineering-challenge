from collections import defaultdict
from datetime import timedelta
import logging

from unbabel.util import get_entry_date

logger = logging.getLogger(__name__)


def process_input(events, window_size):
    """
    Processes the input events and outputs a date index average processing time dictionary
    :param events: List of input events in the format defaultdict(None, {'date': datetime.datetime(2018, 12, 26, 18, 11), 'duration': 20})
    :param window_size: Maximum index dates on the output dictionary
    :return:
    """
    processed_events = defaultdict()
    current_average = 0
    current_date = None
    registered_events = 0
    if events:
        for event in events:
            if "date" in event.keys() and "average_delivery_time" in event.keys():
                processed_events, window_size, registered_events, current_date, current_average = _add_event(
                    event,
                    processed_events,
                    window_size,
                    registered_events,
                    current_date,
                    current_average,
                )
    if registered_events < window_size and current_date:
        processed_events = pad_output(
            processed_events, current_date, current_average, registered_events, window_size
        )
    return processed_events


def pad_output(
    processed_entries, current_date, current_average, registered_events, window_size
):
    """
    Pads the time indexed dictionary if the window size wasn't met
    :param processed_entries: Dictionary of events indexed by date to be padded
    :param current_date: Next date to be added in processed_entries keys
    :param current_average: Current average time
    :param registered_events: Entries already present in the dictionary
    :param window_size: Maximum events to be present in processed_entries
    :return:
    """
    while registered_events < window_size:
        processed_entries[current_date] = current_average
        current_date = current_date + timedelta(minutes=1)
        registered_events = registered_events + 1
    return processed_entries


def _add_event(
    event, processed_events, window_size, number_events, current_date, current_average
):
    """
    Add an entry to the averages dictionary
    :param event: The input Event to be added
    :param processed_events: Dictionary of events indexed by date to which the entry is being added to
    :param window_size: Maximum events to be present in processed_entries
    :param number_events: Events already present in the dictionary
    :param current_date: Next date to be added in processed_entries keys
    :param current_average: Current average time
    :return: Updated values for the input arguments
    """
    start_date, effective_date = get_entry_date(event)
    if not current_date:
        current_date = start_date
    if start_date == current_date:  # initial event go here
        if number_events < window_size:
            processed_events[start_date] = current_average
            number_events = number_events + 1
        if number_events < window_size:
            if current_average > 0:
                current_average = (current_average + event["average_delivery_time"]) / 2
                processed_events[effective_date] = current_average
            else:
                current_average = event["average_delivery_time"]
                processed_events[effective_date] = current_average
            current_date = effective_date
            number_events = number_events + 1
            current_date = current_date + timedelta(minutes=1)
    elif start_date < current_date:  # events on past minutes
        current_average = (
            processed_events[effective_date] + event["average_delivery_time"]
        ) / 2
        processed_events[effective_date] = current_average
    else:  # all other events go here
        while current_date <= effective_date and number_events < window_size:
            if current_date == effective_date:
                if current_average > 0:
                    current_average = (
                        current_average + event["average_delivery_time"]
                    ) / 2
                    processed_events[effective_date] = current_average
                    current_date = effective_date
                    number_events = number_events + 1
            else:
                processed_events[current_date] = current_average
                number_events = number_events + 1
            current_date = current_date + timedelta(minutes=1)
    return processed_events, window_size, number_events, current_date, current_average
