
"""
A module to hold utility functions.
"""


def get_average(events):
    """
    Returns average duration of events.
    """

    average = 0
    total_sum_of_durations = 0
    total_count = 0

    if not len(events):
        return average

    for key in events.keys():
        total_sum_of_durations += events[key]['duration_sum']
        total_count += events[key]['count']

    average = total_sum_of_durations/total_count

    return format_number(average)


def format_number(number):
    """
    Returns an integer if number is a "whole number"
    """
    if number % 1 == 0:
        return int(number)
    return number
