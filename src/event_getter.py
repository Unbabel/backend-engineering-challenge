
"""
Events Getter.
"""


from .factories import EventFactory


class EventGetter:

    """
    An implementation of generators to get events.
    """

    def __init__(self, event_stream, filters={}):
        self.event_stream = event_stream
        self.filters = filters

    def get_events(self):
        """
        Generator function that yields events.
        """

        for event in self.event_stream:
            event = EventFactory.create_event(event)
            if self.should_included(event):
                yield event

    def should_included(self, event):
        """
        Returns true if event qualifies on filtering options
        """

        if not self.filters:
            return True

        for key in self.filters.keys():
            try:
                value_in_event = event[key]
            except KeyError:
                return False
            if str(value_in_event) != self.filters[key]:
                return False

        return True
