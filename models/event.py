from pydantic.dataclasses import dataclass

# DataClass representing the input event, based on Pydantic dataclasses to help with fields validation


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
