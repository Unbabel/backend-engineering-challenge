import argparse
import os
import json
from datetime import datetime, timedelta


class UnbabelCLI(object):
    """
    A class that processes events, generates moving average delivery times every minute within a given window
    """

    def __init__(self, input_file, window_size, output_file="output_data.json"):
        """
        Initializes instance

        :param input_file:
        str: Path to input file
        :param window_size:
        int: Positive integer as window size
        :param output_file:
        str: Optional. Path to output file
        """
        self._input_file = input_file
        self._window_size = window_size
        self._output_file = output_file if output_file else "output_data.json"
        self._date_timestamp_durations_map = {}
        self._highest_window_timestamp = None
        self._lowest_window_timestamp = None

    def _validate_args(self):
        """
        Validates the input_file and window_size arguments values

        :raises:
        ValueError: when invalid values

        :return:
        """
        if not self._input_file or not os.path.exists(self._input_file) or not os.path.isfile(self._input_file):
            raise ValueError("Invalid input file-path value")
        if not self._window_size or self._window_size <= 0:
            raise ValueError("Invalid window size value, should be higher than 0")

    @staticmethod
    def _is_valid_event(event):
        """
        Validates event by checking presence of required model fields in event body

        :param event:
        dict: event body

        :return:
        boolean: True if all required model fields are present in event body else False
        """
        required_model_fields = ['translation_id', 'event_name', 'timestamp', 'duration']
        return all([field in event for field in required_model_fields])

    def _get_next_recent_event(self):
        """
        Yields next most recent event (assuming most recent event is always dumped at the end of input file)

        :return:
        generator object: To iterate over most recent events falling within window
        """

        # define an empty stack as character buffer to form an event body as we read backwards
        chars_stack = []
        buffering_enabled = False
        with open(self._input_file) as fh:
            # read the input file backwards from an end, one character at a time
            fh_position = fh.seek(os.SEEK_SET, os.SEEK_END)
            while fh_position >= 0:
                char = fh.read(1)
                if char == "}":  # start buffering in a stack
                    chars_stack.append(char)
                    buffering_enabled = True
                elif char == "{":  # stop buffering and form event body using buffered content from a stack
                    event_body = json.loads(char + "".join([chars_stack.pop() for _ in range(len(chars_stack))]))
                    if self._is_valid_event(event_body):
                        yield event_body
                    buffering_enabled = False
                elif buffering_enabled:  # keep buffering in a stack as long as buffering is enabled
                    chars_stack.append(char)
                if fh_position == 0:  # beginning of file has reached so stop reading
                    break
                fh_position = fh.seek(fh_position-1)

    def _parse_and_process_events(self):
        """
        Parses events and maps their durations to respective date-timestamps

        :return:
        """
        for event in self._get_next_recent_event():
            event_timestamp = datetime.strptime(event["timestamp"], "%Y-%m-%d %H:%M:%S.%f")

            # ignore seconds and microseconds of event timestamp, resulting timestamp is a date-timestamp
            date_timestamp = event_timestamp - timedelta(
                seconds=event_timestamp.second, microseconds=event_timestamp.microsecond
            )

            # if most recent event of all, set highest and lowest timestamps of window using it
            if self._highest_window_timestamp is None:
                self._highest_window_timestamp = date_timestamp
                self._lowest_window_timestamp = date_timestamp - timedelta(minutes=self._window_size)

            # skip iteration if event timestamp is higher than highest timestamp of window
            if self._highest_window_timestamp < event_timestamp:
                continue

            # break if event timestamp is lower than lowest timestamp of window
            if self._lowest_window_timestamp > event_timestamp:
                break

            # if event timestamp has seconds or microseconds, then its to be mapped to next date-timestamp
            if event_timestamp.second or event_timestamp.microsecond:
                date_timestamp += timedelta(minutes=1)

            # Add the events' duration to the list of durations mapped to this date-timestamp
            if date_timestamp not in self._date_timestamp_durations_map:
                self._date_timestamp_durations_map[date_timestamp] = []
            self._date_timestamp_durations_map[date_timestamp].append(event["duration"])

    def get_average_delivery_time(self, window_date_timestamp):
        """
        Computes an average delivery time for a given date-timestamp

        :param window_date_timestamp:
        datetime: one of the date-timestamps within a given window

        :return:
        int/float: an average delivery time
        """
        delivery_time_sum, delivery_count = 0, 0
        for map_date_timestamp in self._date_timestamp_durations_map:
            # skip map date-timestamp if its higher than window date-timestamp
            if map_date_timestamp > window_date_timestamp:
                continue
            delivery_time_sum += sum(self._date_timestamp_durations_map[map_date_timestamp])
            delivery_count += len(self._date_timestamp_durations_map[map_date_timestamp])

        if delivery_count == 0:  # avoid division by 0 while computing an average delivery time
            return 0
        average = delivery_time_sum / delivery_count
        return float("%.1f" % average) if average % int(average) else int(average)

    def _dump_average_delivery_times(self):
        """
        Computes moving average delivery times every minute within a specified window, dumps them in an output file as
        a stringified JSON
        :return:
        """
        with open(self._output_file, "w") as output_json:
            if not self._highest_window_timestamp:
                return
            for i in range(self._window_size-1, -1, -1):
                window_timestamp = self._highest_window_timestamp - timedelta(minutes=i)
                average_delivery_time = self.get_average_delivery_time(window_timestamp)

                # prepare output dictionary (as json) for this timestamp
                data = {
                    "date": window_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "average_delivery_time": average_delivery_time
                }

                # finally dump average delivery time for this minute timestamp to output file followed by newline char
                output_json.write(json.dumps(data))
                output_json.write("\n")

    def generate_moving_average_delivery_times(self):
        self._validate_args()
        self._parse_and_process_events()
        self._dump_average_delivery_times()


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser("python unbabel_cli.py")
    args_parser.add_argument("-i", "--input_file", help="Path to file containing delivery events", required=True)
    args_parser.add_argument("-w", "--window_size", type=int, help="Number of past minutes to consider", required=True)
    args_parser.add_argument("-o", "--output_file", help="Path to file to store aggregated output data", required=False)

    args = args_parser.parse_args()

    unbabel_cli = UnbabelCLI(args.input_file, args.window_size, args.output_file)
    unbabel_cli.generate_moving_average_delivery_times()
