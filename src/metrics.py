from numbers import Number
from datetime import datetime, timedelta
from queue import Queue

class Metrics:
    def __init__(self, source, window_size, buffer_output=False):
        self.source = source
        self.open = True
        self.buffer_output = buffer_output
        self.buffer = []
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

    def parse_entry(self, entry):
        try:
            assert isinstance(entry['duration'], Number)
            new_time = self.parse_time(entry['timestamp'])
        except:
            raise AssertionError('Entry {} has invalid duration'.format(entry))
        if new_time < self.current['time']:
            raise AssertionError('Entry {} is out of order'.format(entry))
        return new_time, entry['duration']

    def read_source(self):
        try:
            entry = next(self.source)
            new_time, duration = self.parse_entry(entry)
        except StopIteration:
            new_time = self.current['time'] + timedelta(minutes=1)
            duration = 0
            self.open = False
        except:
            raise AssertionError('Failed to read source')
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
        if self.buffer_output:
            self.buffer.append(metrics)
        else:
            print(metrics)

    def flush_buffer(self):
        for entry in self.buffer:
            print(entry)
        self.buffer = []