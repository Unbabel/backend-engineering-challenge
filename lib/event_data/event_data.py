import json
from datetime import datetime


class EventData:

  def __init__(self, data):
      self.__dict__ = self.create_event_data(data)

  def create_event_data(self, data):
      data["timestamp"] = datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
      return data
