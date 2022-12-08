from pydantic.dataclasses import dataclass
from datetime import datetime

# DataClass representing the input event, based on Pydantic dataclasses to help with fields validation


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
