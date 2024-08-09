# Unbabel Backend Engineering Challenge - Sequential Processing Approach

This project implements a sequential processing approach to calculate the moving average of translation delivery times. It processes events in chronological order using a sliding window, designed for memory efficiency and simplicity.

## Features

- **Sequential Processing**: Efficiently processes events in order.
- **Memory Efficiency**: Utilizes a deque for managing the sliding window.
- **Comprehensive Error Handling**: Robust error handling for file operations and JSON parsing.
- **Logging**: Provides detailed logging for tracking execution and debugging.


## Requirements

- Python 3.7 or higher
- pandas

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/komalparakh05/backend-engineering-challenge.git
   cd backend-engineering-challenge


2. Create a virtual environment and install dependencies:

	```bash
 	python -m venv venv
	.\venv\Scripts\activate  # On Windows
	# source venv/bin/activate  # On macOS/Linux
	pip install -r requirements.txt


## Usage

Run the script with the following command:

	
	python unbabel_cli.py --input_file <path_to_input_file> --window_size <window_size_in_minutes> [--chunk_size <chunk_size>]

Example:

	
	python unbabel_cli.py --input_file events.json --window_size 10 --chunk_size 50000


## Testing

To test the code, you can create unit tests using a framework like unittest or pytest. Ensure your tests cover key functionalities such as parsing input, calculating averages, and handling errors. Here's how to set up pytest:

Install pytest:

	
	pip install pytest

Run tests using:

	
	pytest

**Refer to the `test_unbabel_cli.py` script for details on how to use `pytest`.**


## Design Considerations

- **Order of Processing**: Designed to efficiently handle ordered input data.
- **Memory Optimization**: Uses a deque to minimize memory usage while managing the sliding window.
- **Error Resilience**: Incorporates error handling to ensure robust execution.
- **Transparency**: Provides logging to help understand the processing flow and diagnose issues..


## Alternative Approach

An alternative approach that focuses on streaming processing and real-time data handling is available in the `streaming_approach` branch. 

To explore this alternative approach, check out the `streaming_approach` branch:

git checkout streaming_approach

This alternative solution showcases additional data engineering skills and provides a more comprehensive approach to the challenge.
