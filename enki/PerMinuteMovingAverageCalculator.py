from datetime import datetime, timedelta

from enki.MovingAverageCalculator import MovingAverageCalculator


class PerMinuteMovingAverageCalculator(MovingAverageCalculator):
    """
    Data must be sorted w.r.t. get_bucket_key(data).
    Moving average of a bucket will be emitted when get_bucket_key(data) changes
    or when the stream ends.

    Buckets that do not have data, does not affect the moving average.

    Example:
    "2018-12-26 18:11:00": 10
    "2018-12-26 18:13:00": 20

    would yield three values for the moving average for a window size greater
    than or equal to 2: [10, 10, 15]
    """

    emitted_initial = False

    def emit_bucket(self, bucket):
        # Between the previous bucket and current bucket, emit None values so we
        # could use MovingAverageRing.get_populated_average method to get the result.

        current = datetime.fromisoformat(bucket)
        if self.prev_bucket_key is not None:
            prev = datetime.fromisoformat(self.prev_bucket_key)

        # Emit an initial data.
        if not self.emitted_initial:
            self.emit({
                self.timestamp_key: self.prev_bucket_key,
                self.result_key: self.ring.get_populated_average(),
            })
            self.emitted_initial = True

        self.ring.append(self.bucket_sum)

        self.emit({
            self.timestamp_key: (prev + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"),
            self.result_key: self.ring.get_populated_average(),
        })

        self.bucket_sum = 0

        if self.prev_bucket_key is not None:
            delta_minutes = int((current - prev).total_seconds() / 60)
            if delta_minutes < 0:
                raise ValueError("Timestamps must be sorted.")

            # For every minute that did not have any data points, add a None and emit.
            for i in range(1, delta_minutes):
                bucket_date = prev + timedelta(minutes=i+1)
                bucket = bucket_date.strftime("%Y-%m-%d %H:%M:%S")
                self.ring.append(None)
                self.emit({
                    self.timestamp_key: bucket,
                    self.result_key: self.ring.get_populated_average(),
                })

        self.has_data = False

    def end(self):
        super().end()
