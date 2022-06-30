import src.util.util as util


def process(events, window_size):
    events = iter(events)
    event = next(events)
    moving_average = []
    delta_records = {}

    start_of_range = _get_start_of_range(delta_records, event['datetime'])
    end_of_range = _get_end_of_range(start_of_range, window_size)

    current_minute = start_of_range
    first_moving_average = _get_output_for_minute(current_minute, delta_records)

    moving_average.append(first_moving_average)

    delta_records[start_of_range] = {"count": 1, "duration": event['duration']}

    current_minute = util.add_minutes(current_minute, 1)

    current_minute, delta_records = _calculate_moving_average(current_minute, end_of_range, events, delta_records,
                                                                 moving_average, start_of_range, window_size)

    moving_average.append(_get_output_for_minute(current_minute, delta_records))

    return moving_average


def _get_output_for_minute(timestamp, events):
    average_delivery_time = util.get_average(events)
    timestamp = util.get_string_from_datetime(timestamp)

    return {"date": timestamp, "average_delivery_time": average_delivery_time}


def _get_start_of_range(events, datetime):
    if len(events):
        return [key for key in events.keys()][0]

    return datetime


def _get_end_of_range(start_range, window_size):
    return util.add_minutes(start_range, window_size)


def _get_adjusted_window(events, star_of_range):
    events.pop(star_of_range)
    return events


def _calculate_moving_average(current_minute, end_of_range, events, events_in_window, moving_average, start_of_range,
                              window_size):
    for event in events:

        event_timestamp = event['timestamp']
        event_rounded_timestamp = event['datetime']

        if event_timestamp >= current_minute:

            next_minutes_count = util.get_difference_in_number_of_minutes(
                event_rounded_timestamp, current_minute)
            next_minutes_count += 1

            for i in range(int(next_minutes_count)):

                moving_average_per_minute = _get_output_for_minute(
                    current_minute, events_in_window)
                moving_average.append(moving_average_per_minute)

                current_minute = util.add_minutes(
                    current_minute, 1)

                if current_minute > end_of_range:
                    events_in_window = _get_adjusted_window(
                        events_in_window, start_of_range)
                    start_of_range = _get_start_of_range(
                        events_in_window, event_rounded_timestamp)
                    end_of_range = _get_end_of_range(
                        start_of_range, window_size)

        if events_in_window.get(event_rounded_timestamp, None):
            events_in_window[event_rounded_timestamp]['count'] += 1
            events_in_window[event_rounded_timestamp]['duration'] += event['duration']
        else:
            events_in_window[event_rounded_timestamp] = {"count": 1, "duration": event['duration']}
    return current_minute, events_in_window
