import json
from typing import Callable, TypeVar

from enki.StreamProcessor import StreamProcessor

T = TypeVar("T")


class Filter(StreamProcessor[T, T]):
    predicate: Callable[[T], bool]

    def __init__(self, sink: Callable[[T], None], predicate: Callable[[T], bool]):
        super().__init__(sink)
        self.predicate = predicate

    def consume(self, data: T):
        """
        Data is single object of JSON.
        """
        if self.predicate(data):
            self.emit(data)
