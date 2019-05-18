import json

def file_input_reader(filename):
    with open(filename, 'r') as f:
        result = f.readline()
        if not result:
            raise AssertionError('File is empty')
        while result:
            yield json.loads(result)
            result = f.readline()

import pytest

def test_valid():
    for file_name in ('basic', 'out_of_order', 'wrong_type'):
        f = file_input_reader('./test_cases/{}.json'.format(file_name))
        for _ in range(3):
            next(f)
        with pytest.raises(StopIteration):
            next(f)

def test_empty():
    f = file_input_reader('./test_cases/empty.json')
    with pytest.raises(AssertionError):
        next(f)

def test_malformed():
    f = file_input_reader('./test_cases/malformed.json')
    next(f)
    with pytest.raises(json.JSONDecodeError):
        next(f)
        