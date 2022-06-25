import argparse
from datetime import timedelta
import json
import sys

from Entry import Entry

average_dict = []
minute_list = []

# INITIATE ARGUMENT PARSER
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str)
parser.add_argument('--window_size', type=int)

# STORE ARGUMENTS IN VARIABLES 
args = parser.parse_args()
filename = args.input_file
window_size=args.window_size

try:
    input_file = open(filename, 'r')
except OSError:
    print("Could not open/read file:", filename)
    sys.exit()

with input_file:
    input_data = json.loads(input_file.read())
    for row in input_data:
        minute_list.append(Entry(minute=row['timestamp'], duration=row['duration'])) # append each entry from json into the minutes dict before filling in the "gaps"

# Fill in the "missing" minutes
for i in range(len(minute_list)-1):
    # TODO
    pass    
