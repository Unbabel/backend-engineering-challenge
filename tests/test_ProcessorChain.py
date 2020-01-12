import unittest

from enki.Filter import Filter
from enki.JsonDumper import JsonDumper
from enki.JsonParser import JsonParser
from enki.PerMinuteMovingAverageCalculator import PerMinuteMovingAverageCalculator
from enki.ProcessorChain import ProcessorChain


class TestProcessorChain(unittest.TestCase):
    def test_json_roundtrip(self):
        items = []

        def add(item):
            items.append(item)

        chain = ProcessorChain(add,
                               [
                                   lambda sink: JsonParser(sink),
                                   lambda sink: JsonDumper(sink),
                               ])

        chain.consume("{  }")

        self.assertEqual(["{}"], items)

    def test_example(self):
        items = []

        def add(item):
            items.append(item)

        chain = ProcessorChain(add,
                               [
                                   lambda sink: JsonParser(sink),
                                   lambda sink: PerMinuteMovingAverageCalculator(
                                       sink,
                                       10,
                                       lambda x: "%s:00" % x["timestamp"][:16],
                                       lambda x: x["duration"], "date", "average_delivery_time"),
                                   lambda sink: JsonDumper(sink),
                               ])

        chain.consume(
            '{"timestamp": "2018-12-26 18:11:08.509654", "duration": 20}')
        chain.consume(
            '{"timestamp": "2018-12-26 18:15:19.903159", "duration": 31}')
        chain.consume(
            '{"timestamp": "2018-12-26 18:23:19.903159", "duration": 54}')

        chain.end()

        self.assertEqual([
            '{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}',
            '{"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0}',
            '{"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0}',
            '{"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0}',
            '{"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0}',
            '{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}',
            '{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}',
        ], items)

    def test_example_with_filter(self):
        items = []

        def add(item):
            items.append(item)

        chain = ProcessorChain(add,
                               [
                                   lambda sink: JsonParser(sink),
                                   lambda sink: Filter(sink, lambda x: x["duration"] > 20),
                                   lambda sink: PerMinuteMovingAverageCalculator(
                                       sink,
                                       10,
                                       lambda x: "%s:00" % x["timestamp"][:16],
                                       lambda x: x["duration"], "date", "average_delivery_time"),
                                   lambda sink: JsonDumper(sink),
                               ])

        chain.consume(
            '{"timestamp": "2018-12-26 18:11:08.509654", "duration": 20}')
        chain.consume(
            '{"timestamp": "2018-12-26 18:15:19.903159", "duration": 31}')
        chain.consume(
            '{"timestamp": "2018-12-26 18:23:19.903159", "duration": 54}')

        chain.end()

        self.assertEqual([
            '{"date": "2018-12-26 18:15:00", "average_delivery_time": 0}',
            '{"date": "2018-12-26 18:16:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:17:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:18:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:19:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:20:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:21:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}',
            '{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}'
        ], items)
