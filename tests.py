from src.io import load_events, UnknownFormatError, export_averages
from src.processing import moving_averages, _round_to_minute
import pytest
from pandas import DataFrame
from datetime import datetime


def test_load_events():
    events = load_events("example_events.json")
    assert len(events) == 3


def test_unknown_format(tmpdir):
    filepath = tmpdir.strpath + "/fake.json"

    with open(filepath, "w+") as f:
        f.write("this will break the test")

    with pytest.raises(UnknownFormatError):
        load_events(filepath)


def test_moving_averages():
    timestamps = DataFrame(
        data={
            "timestamp": [
                datetime(year=1, month=1, day=1, minute=1, second=1),
                datetime(year=1, month=1, day=1, minute=5, second=1),
                datetime(year=1, month=1, day=1, minute=5, second=3),
            ],
            "duration": [1, 40, 20],
        }
    )
    averages = moving_averages(timestamps, window_size=1)

    assert len(averages) == 6
    assert averages[3].get("average_delivery_time") == 0
    assert averages[1].get("average_delivery_time") == 1
    assert averages[5].get("average_delivery_time") == 30
    assert averages[5].get("date") == datetime(year=1, month=1, day=1, minute=6)


def test_round_to_minute():
    test_times = [
        datetime(year=2019, month=2, day=1, minute=3),
        datetime(year=2019, month=2, day=1, minute=3, second=4),
    ]

    expected_up = [
        datetime(year=2019, month=2, day=1, minute=3),
        datetime(year=2019, month=2, day=1, minute=4),
    ]

    expected_down = [
        datetime(year=2019, month=2, day=1, minute=3),
        datetime(year=2019, month=2, day=1, minute=3),
    ]

    for i, time in enumerate(test_times):
        assert _round_to_minute(time, upwards=True) == expected_up[i]
        assert _round_to_minute(time, upwards=False) == expected_down[i]


def test_integration(tmpdir):
    filepath = tmpdir.strpath + "/output.json"
    timestamps = load_events("example_events.json")

    averages = moving_averages(timestamps, 10)
    export_averages(averages, filepath)

    with open(filepath, "r") as f:
        output = f.read()

    with open("example_output.json", "r") as f:
        expected = f.read()

    assert output == expected
