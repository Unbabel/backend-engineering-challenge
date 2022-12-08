from pydantic.dataclasses import dataclass

# DataClass Representing the output event


@dataclass
class AverageDevlieryEvent():
    date: str
    average_delivery_time: float
