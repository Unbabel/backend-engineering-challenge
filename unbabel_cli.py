from typing import NamedTuple, Deque, TextIO
from json import loads
from math import floor
from datetime import datetime
from collections import deque

class Event(NamedTuple):
    epoch_minute: int
    duration: int
    
    @classmethod
    def from_input_line(cls, input_line: str):
        """
        Creates a new Event instance from an event string read from the file

        Args:
            input_line: The event string read from the file

        Returns:
            Event instance 
        """
        event_json = loads(input_line)
        event = cls(floor(int(datetime.fromisoformat(event_json["timestamp"]).timestamp())/60),
                     event_json["duration"])
        
        print(f"CREATING event: {event}")

        return event

class Window:
    def __init__(self, size: int, initial_epoch_minute: int):
        """
        Initializes a new sliding window

        Args:
            size: The size of the sliding window
            initial_epoch_minute: The epoch minute of the first event
        """
        self.__size: int = size
        self.__events: Deque[Event] = deque()
        self.__start: int = initial_epoch_minute - self.__size
        self.__agg_duration: int = 0

    def add_event(self, event: Event):
        """
        Adds an event to the window events list and updates the aggregated duration

        Args:
            event: The event read from the input file
        """
        self.__events.append(event)
        self.__agg_duration += event.duration

    def slide(self):
        """
        Slides the window removing events outside the window and updating the aggregated duration
        """
        self.__start += 1

        print(f"START: {self.__start}")
        
        counter = 0
        for event in self.__events:
            #count the number of events to be removed
            if event.epoch_minute < self.__start:
                counter += 1
            else:
                break

        for _ in range(counter):
            """
            since the deque is ordered by event epoch_minute we just need to remove the "counter"
            first elements from the head of the queue
            """
            event = self.__events.popleft()
            self.__agg_duration -= event.duration

        print(f"START: {self.__events}")
    
    def is_event_outside_window(self, event: Event):
        """
        Determines if an event is outside the window

        Args:
            event: The event read from the input file
        
        Returns:
            bool
        """
        return event.epoch_minute > self.__start + self.__size - 1
    
    def __calculate_average_delivery_time(self):
        """
        Calculates the average delivery time for the window events

        Returns:
            The average delivery time
        """
        if self.__agg_duration == 0:
            return 0

        return self.__agg_duration / len(self.__events)

    def __str__(self):
        return (
            f"{{\"date\":\"{datetime.fromtimestamp((self.__start + self.__size)*60).strftime('%Y-%m-%d %H:%M:%S')}\", "
            f"\"average_delivery_time\":{self.__calculate_average_delivery_time()}}}"
        )
    
def write_to_output_with_new_line(output: TextIO, window: Window):
    output.write(str(window))
    output.write("\n")
        
def main():
    """
    """
    size = 10

    with open("events.json", "r", encoding="utf-8") as input:
        with open("output.json", "w", encoding="utf-8") as output:
            initial_event = Event.from_input_line(input.readline())

            window = Window(size, initial_event.epoch_minute)
            write_to_output_with_new_line(output, window)
            window.slide()
            window.add_event(initial_event)

            for line in input:
                event = Event.from_input_line(line)

                while window.is_event_outside_window(event):
                    write_to_output_with_new_line(output, window)
                    window.slide()

                window.add_event(event)
                
            else:
                output.write(str(window))

if __name__ == "__main__":
    main()