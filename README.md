# Unbabel cli
simple command line application that parses a stream of events and produces an aggregated output. In this case, we're instered in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

### Run
`cd cli`
`python unbabel_cli.py --input_file ../data/inputs/input.json  --window_size 10`

### Run tests
`python -m pytest cli/tests/`
