# UnbabelCLI

Microservice to process and export metrics for translation service latency.

### Installation
* run pip install -e ./

### Run
* unbabel_cli --input_file src/test_cases/basic.json --window_size 10

### Tests
* cd src && pytest main.py

### TODO
* edge cases
* fuzzing
* support non-file based inputs (pubsub)
* dockerize and output results to prometheus supported endpoint

License
----

MIT