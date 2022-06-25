import argparse
from datetime import datetime, timedelta
import json
import sys

from Entry import Entry

average_dict = []
received_times = []
date_list = []

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
    # Print custom message if file is not found
    print("Could not open/read file:", filename)
    sys.exit()

with input_file:
    input_data = json.loads(input_file.read())
    for row in input_data:
        received_times.append(Entry(date=row['timestamp'], duration=row['duration'])) # append each entry from json into the minutes dict before filling in the "gaps"

# Fill in the "missing" minutes
for i in range(len(received_times)):
    
    # Append the received time to the final list
    date_list.append(received_times[i])
    
    # if we are on the last position, add one more minute and go to next position
    if i == len(received_times) - 1:
        new_entry = Entry(str(received_times[i].date + timedelta(minutes=1)), duration = 0)
        date_list.append(new_entry)
    
    # else, calculate difference (gap) between the two positions and add the missing numbers to the final list
    else:
        # calculating gap
        gap = received_times[i+1].date - received_times[i].date
        
        x = 1
        while x < (gap.total_seconds()/60)-1:
            new_entry = Entry(str(received_times[i].date + timedelta(minutes=x)), duration = 0)
            date_list.append(new_entry)
            x+=1

print(date_list) 
