from datetime import datetime, timedelta
from Queue import Queue

class Metrics:
    def __init__(self, source, window_size):
        self.source = source
        self.open = True
        self.count = 0
        self.sum = 0
        self.history = Queue(window_size)
        self.current = None
        self.reset_current()

    @staticmethod
    def parse_time(time_string):
        return datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f')

    def reset_current(self, time=datetime.min):
        self.current = {'count': 0, 'sum': 0, 'time': time}

    def run(self):
        while self.open:
            self.next()

    def read_source(self):
        try:
            entry = self.source.next()
            new_time = self.parse_time(entry['timestamp'])
            if new_time < self.current['time']:
                raise AssertionError('Entries given out of order')
            duration = entry['duration']
        except StopIteration:
            new_time = self.current['time'] + timedelta(minutes=1)
            duration = 0
            self.open = False
        return new_time, duration

    def next(self):
        new_time, duration = self.read_source()
        self.handle_metrics(new_time)
        self.current['count'] += 1
        self.current['sum'] += duration

    def handle_metrics(self, new_time):
        while self.should_output(new_time):
            if self.current['time'] == datetime.min:
                self.current['time'] = new_time.replace(second=0, microsecond=0)
            self.output_metrics()
            self.reset_current(self.current['time'] + timedelta(minutes=1))

    def should_output(self, new_time):
        return new_time.minute > self.current['time'].minute

    def calculate_metrics(self):
        if self.history.full():
            leaver = self.history.get()
            self.count -= leaver['count']
            self.sum -= leaver['sum']
        self.count += self.current['count']    
        self.sum += self.current['sum']
        self.history.put(self.current)
        return self.sum/float(self.count or 1)

    def output_metrics(self):
        average_delivery_time = self.calculate_metrics()
        date_string = datetime.strftime(self.current['time'], '%Y-%m-%d %H:%M:%S')
        metrics = {'date': date_string, 'average_delivery_time': average_delivery_time}
        print(metrics)
        return metrics
