# Backend Engineering Challenge -- Moving Average Calculator

## Overview

This Python script calculates the moving average delivery time based on events read from a JSON file. The moving average is computed over a specified time window.

## Requirements

* Python 3.x
* Dependencies (install via `pip install -r requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thisIsMailson/moving-average-calculator.git
cd moving-average-calculator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

# Usage

To calculate the moving average delivery time, run the script with the input JSON file and window size. Example:
```bash
python3 main.py --input_file=input.json --window_size=10
```
* input_file: Path to the input JSON file.
* window_size: Size of the time window for the moving average.

The results will be saved to an output file.

# Running Tests
```bash
python -m unittest events_test.py 
```

## Sample Data

For testing purposes, you can use the provided sample JSON file sample_data.json.

# File Structure

 * calculate_moving_average.py: Main script for calculating the moving average.
 * test_calculate_moving_average.py: Test cases for the script.
 * sample_data.json: Sample input data for testing.
