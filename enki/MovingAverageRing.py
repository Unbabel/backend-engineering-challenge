from collections import deque
from typing import Optional


class MovingAverageRing:
    q: deque
    ma_sum: float
    count: int  # count of items in the deque.
    population: int  # count of items that are not None in the deque.

    def __init__(self, window: int):
        if window <= 0:
            raise ValueError("window must be greater that 0.")

        self.q = deque([], window)
        self.ma_sum = 0
        self.count = 0
        self.population = 0

        # Fill with Nones so deque is full but population is zero.
        for i in range(window):
            self.q.append(None)

    def get(self) -> float:
        """
        Get moving average.
        """

        if self.count == 0:
            return 0
        return self.ma_sum / self.count

    def get_populated_average(self) -> float:
        """
        Get moving average excluding empty slots.
        """

        if self.count == 0 or self.population == 0:
            return 0

        return self.ma_sum / self.population

    def append(self, value: Optional[float]) -> None:
        leaving = self.q.popleft()
        self.q.append(value)

        if leaving is not None:
            self.ma_sum -= leaving
            self.population -= 1

        if value is not None:
            self.ma_sum += value
            self.population += 1

        if self.count != self.q.maxlen:
            self.count += 1
