# Backend Engineering Challenge

Thanks for reviewing my solution.

This package contains code for computing moving averages of an events stream and exporting them to a specific format.  An example of the input/output files are given as `example_events.json` and `example_output.json`.

## Quickstart

To run the CLI, you will need to execute

```
cd backend-engineering-challenge
pip install -e .
```

Then the following command will work for an arbitrary `events.json` and `window_size`:

```
unbabel_cli --input_file <events.json> --window_size <window_size>
```

Alternatively you can install and run using Python with

```
cd backend-engineering-challenge
pip install -r requirements.txt
python main.py --input_file <events.json> --window_size <window_size>
```

## Tests

To run the test suite, install requirements as above and run:

```
cd backend-engineering-challenge
pytest tests.py
```