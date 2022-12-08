from pydantic.dataclasses import dataclass
from datetime import datetime

"""
    Dataclass representing an event object
"""


@dataclass
class Event():
    timestamp: datetime
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    event_name: str
    duration: int
    nr_words: int
