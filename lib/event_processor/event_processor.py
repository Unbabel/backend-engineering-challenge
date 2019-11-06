import os.path
import math
import time
import json
from lib.event_data.event_data import EventData
from lib.event_reader.event_reader import EventReader
from datetime import datetime
from datetime import timedelta
from functools import reduce


class EventProcessor:
    def __init__(self, file, event_validator):
        self.file = file
        self.event_validator = event_validator
        
        self.event_list = []
        self.event_errors_found = []
        self.read_file()
        self.order_list()
    
    def read_file(self):
        with open(self.file) as file_read:
            self.stream_events_to_list(file_read)

    def stream_events_to_list(self, file_read):
        for line in file_read:
            event_data = json.loads(line.rstrip('\n'))

            if not self.event_validator.validate(event_data):
                self.event_errors_found.append(
                    "The event " + event_data.get('translation_id') + 
                    " has invalid data, check the timestamp or duration"
                )
            else:
                self.event_list.append(EventData(event_data))

    def order_list(self):
        self.event_list.sort(key=lambda event: event.timestamp, reverse=False)

        return self.event_list
    
    def calculate_date_range(self, window_size):
        event_list = self.event_list
        first_datetime = self.__get_first_date_range(event_list[0].timestamp)
        last_datetime = self.__get_last_date_range(event_list[-1].timestamp)

        difference_in_seconds = time.mktime(last_datetime.timetuple())-time.mktime(first_datetime.timetuple())
        difference_in_minutes = math.ceil((difference_in_seconds/60))

        output = []
        for index in range(difference_in_minutes+1):
            start_date = first_datetime + timedelta(minutes=index) 
            end_date = start_date + timedelta(minutes=-window_size)

            average = self.calculate_average_delivery_time( 
              start_date,
              end_date
            )

            output.append({
              'date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
              'average_delivery_time': average
            })
        return output

    def calculate_average_delivery_time(self, start_date, end_date):
        list_filtered = list(
          filter(
            lambda event: 
                event.timestamp >= end_date and event.timestamp <= start_date,
            self.event_list
          )
        )
        
        if len(list_filtered) == 0:
          return 0

        if len(list_filtered) == 1:
          return list_filtered[0].duration

        total = reduce(
            (lambda x, y:  x.duration + y.duration), 
            list_filtered
        )
        
        return total/len(list_filtered)
   
    def get_events_with_invalid_data(self):
        return self.event_errors_found
    
    def get_events_list(self):
        return self.event_list

    def __get_first_date_range(self, date):
        if  date.second > 0 or date.microsecond > 0:
            return datetime(
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute
            )

        return date

    def __get_last_date_range(self, date):
        if  date.second > 0 or date.microsecond > 0:
            return datetime(
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute+1
            )

        return date
        