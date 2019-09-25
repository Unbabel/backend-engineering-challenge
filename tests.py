from src.loading import load_timestamps, UnknownFormatError
import pytest
from datetime import timedelta


def test_load_timestamps():
    timestamps = load_timestamps('events.json')

    assert len(timestamps) == 3
    assert type(timestamps[2] - timestamps[1]) is timedelta


def test_unknown_format(tmpdir):
    filepath = tmpdir.strpath + "/fake.json"

    with open(filepath, 'w+') as f:
        f.write('this will break the test')

    with pytest.raises(UnknownFormatError):
        load_timestamps(filepath)
