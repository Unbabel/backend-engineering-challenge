from typing import Callable, Optional

from enki.MovingAverageRing import MovingAverageRing
from enki.StreamProcessor import StreamProcessor


class MovingAverageCalculator(StreamProcessor[dict, dict]):
    """
    Data must be sorted w.r.t. get_bucket_key(data).
    Moving average of a bucket will be emitted when get_bucket_key(data) changes
    or when the stream ends.

    Example:
    "2018-12-26 18:11:00": 10
    "2018-12-26 18:13:00": 20

    would yield two values for the moving average for a window size greater
    than or equal to 2: [10, 15]
    """

    ring: MovingAverageRing
    get_bucket_key: Callable[[dict], str]
    get_value: Callable[[dict], float]
    prev_bucket_key: Optional[str]
    bucket_sum: float
    has_data: bool

    def __init__(self, sink: Callable[[dict], None], window_size: int,
                 get_bucket_key: Callable[[dict], str], get_value: Callable[[dict], float],
                 timestamp_key: str, result_key: str):
        super().__init__(sink)
        self.ring = MovingAverageRing(window_size)
        self.prev_bucket_key = None
        self.get_bucket_key = get_bucket_key
        self.get_value = get_value
        self.bucket_sum = 0
        self.timestamp_key = timestamp_key
        self.result_key = result_key
        self.has_data = False

    def consume(self, data: dict):
        """
        Data is single object of JSON.
        """

        bucket_key = self.get_bucket_key(data)
        value = self.get_value(data)

        if self.prev_bucket_key is not None and self.prev_bucket_key != bucket_key:
            self.emit_bucket(bucket_key)

        self.bucket_sum += value
        self.prev_bucket_key = bucket_key
        self.has_data = True

    def emit_bucket(self, bucket):
        self.ring.append(self.bucket_sum)

        self.emit({
            self.timestamp_key: self.prev_bucket_key,
            self.result_key: self.ring.get(),
        })

        self.bucket_sum = 0
        self.has_data = False

    def end(self):
        if self.has_data:
            self.emit_bucket(self.prev_bucket_key)
