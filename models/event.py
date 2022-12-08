from pydantic.dataclasses import dataclass


@dataclass
class Event():
    timestamp: str
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    event_name: str
    duration: int
    nr_words: int
