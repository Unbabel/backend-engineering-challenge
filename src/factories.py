"""
Contains factories.
"""

import json
import logging
import src.datetime_manager as datetime_manager


class EventFactory:
    """
    A factory class to handle event creation.
    """

    @staticmethod
    def create_event(event):
        """
        Returns an event model (of type dict).
        """

        required_fields = ['timestamp', 'duration']
        event = json.loads(event)
        try:
            __, __ = event['timestamp'], event['duration']
        except KeyError:
            logging.error(
                "Field is missing. Required fields are: %s", required_fields)
            raise

        event["timestamp"] = datetime_manager.get_datetime_from_string(
            event.get("timestamp"))

        # set any extra fields on model
        event["rounded_timestamp"] = datetime_manager.get_rounded_off_datetime(
            event.get("timestamp"))

        return event
