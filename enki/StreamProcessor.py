from typing import Generic, Callable, TypeVar
from abc import ABC, abstractmethod

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class StreamProcessor(ABC, Generic[TIn, TOut]):
    sink: Callable[[TOut], None]

    def __init__(self, sink: Callable[[TOut], None]):
        self.sink = sink

    @abstractmethod
    def consume(self, data: TIn):
        pass

    def end(self):
        pass

    def emit(self, data: TOut):
        self.sink(data)
