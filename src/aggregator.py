"""
Core application logic
"""


import json
import src.datetime_manager as datetime_manager
from .utility import get_average


class AverageAggregator:

    """
    Aggregator class which calculates running average.
    """

    def __init__(self, events, window_size, output_stream):
        self.events = events
        self.window_size = window_size
        self.output_stream = output_stream

    def create_per_minute_averages(self):
        """
        Calculates aggregated average for events. 
        """

        events_in_window = {}
        event = next(self.events)

        start_of_range = self._get_start_of_range(
            events_in_window, event['rounded_timestamp'])

        end_of_range = self._get_end_of_range(
            start_of_range, self.window_size
        )
        current_minute = start_of_range
        average_for_first_minute = self._get_output_for_minute(
            current_minute, events_in_window)

        self._add_to_output(average_for_first_minute)

        events_in_window[start_of_range] = {
            "count": 1, "duration_sum": event['duration']
        }

        current_minute = datetime_manager.add_minutes(current_minute, 1)

        for event in self.events:

            event_timestamp = event['timestamp']
            event_rounded_timestamp = event['rounded_timestamp']

            if event_timestamp >= current_minute:

                next_minutes_count = datetime_manager.get_difference_in_number_of_minutes(
                    event_rounded_timestamp, current_minute)
                next_minutes_count += 1

                for i in range(int(next_minutes_count)):

                    output_for_minute = self._get_output_for_minute(
                        current_minute, events_in_window)
                    self._add_to_output(output_for_minute)

                    current_minute = datetime_manager.add_minutes(
                        current_minute, 1)

                    if current_minute > end_of_range:
                        events_in_window = self._get_adjusted_window(
                            events_in_window, start_of_range)
                        start_of_range = self._get_start_of_range(
                            events_in_window, event_rounded_timestamp)
                        end_of_range = self._get_end_of_range(
                            start_of_range, self.window_size)

            if events_in_window.get(event_rounded_timestamp, None):
                events_in_window[event_rounded_timestamp]['count'] += 1
                events_in_window[event_rounded_timestamp]['duration_sum'] += event['duration']
            else:
                events_in_window[event_rounded_timestamp] = {
                    "count": 1, "duration_sum": event['duration']}

        average_for_last_timestamp = self._get_output_for_minute(
            current_minute, events_in_window)
        self._add_to_output(average_for_last_timestamp)

        return

    def _get_output_for_minute(self, timestamp, events):
        """
        Returns output for given minute.
        """

        average_delivery_time = get_average(events)
        timestamp = datetime_manager.get_string_from_datetime(timestamp)

        return json.dumps({"date": timestamp, "average_delivery_time": average_delivery_time})

    def _get_start_of_range(self, events, timestamp):
        """
        Returns start of a range.
        """

        if len(events):
            return [key for key in events.keys()][0]

        return timestamp

    def _get_end_of_range(self, start_range, window_size):
        """
        Returns end of range.
        End of range is the last minute of current running range.
        """

        return datetime_manager.add_minutes(start_range, window_size)

    def _get_adjusted_window(self, events, star_of_range):
        """
        Returnd adjusted window. It removes all events included in previous range.
        """

        events.pop(star_of_range)
        return events

    def _add_to_output(self, average_for_minute):
        """
        **File writing shouldn't be done here.**

        This tradeoff is to avoid a very large list of calculated averages for minutes in memory.

        TODO: Find a better way to add output to file
        """
        print(average_for_minute, file=self.output_stream)
