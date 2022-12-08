from pydantic.dataclasses import dataclass
from datetime import datetime


@dataclass
class OutputEvent():
    date: str
    average_delivery_time: float
