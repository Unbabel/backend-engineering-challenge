import argparse
from datetime import timedelta
import json
import sys

from Entry import Entry

average_list = []
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

# Helper function that will add the missing minutes between each minute of the input file
def fill_gaps(received_times, date_list):
    
    for i in range(len(received_times)):
    
        # Append the received time to the final list
        date_list.append(received_times[i])
        
        # if we are on the last position, add one more minute and go to next position
        if i == len(received_times) - 1:
            new_entry = Entry(str(received_times[i].date + timedelta(minutes=1)), duration = 0)
            date_list.append(new_entry)
        
        # else, calculate difference (gap) between the two positions and add the missing numbers to the final list
        else:
            # calculating number of minutes missing between current date and the next date
            gap = received_times[i+1].date - received_times[i].date
            
            # add missing entries to the date_list
            x = 1
            while x < (round(gap.total_seconds()/60)):
                new_entry = Entry(str(received_times[i].date + timedelta(minutes=x)), duration = 0)
                date_list.append(new_entry)
                x+=1

# Helper function to format the entry date to the desired output date format
def format_date(entry):
    return str(entry.date.strftime("%Y-%m-%d %H:%M:%S"))

def write_results(average_list):
    with open('output.json', 'w') as f:
        json.dump(average_list, f)

# Reading the input file
try:
    input_file = open(filename, 'r')
except OSError:
    # Print custom message if file is not found
    print("Could not open/read file:", filename)
    sys.exit()

with input_file:
    # Read input file
    input_data = json.loads(input_file.read())
    # For each row on the input file, create a new Entry object and append it to the received_times list
    for row in input_data:
        received_times.append(Entry(date=row['timestamp'], duration=row['duration']))


# Fill in the "missing" minutes
fill_gaps(received_times, date_list)

# Calculate the moving average for each date in the date_list list
for date in date_list:
    # If we are on the first element, we can assume that the average_delivery_time will be 0, as there are no entries before this one
    if date_list.index(date) == 0:
        average_list.append({
        "date": format_date(date),
        "average_delivery_time": 0
        })
        continue

    # Initialize a counter that will start "window_size" elements before the current entry
    i = date_list.index(date) - window_size
    # Variable that will count the number of entries with a duration != 0 (entries to be considered)
    entries = 0
    # Variable to sum the duration of the entries
    total_sum = 0.0
    # Final average for each date
    average = 0
    
    # While the counter doesn't reach the current date:
    while i < date_list.index(date):
        # Only consider the dates that are in the array
        if i >= 0:
            if date_list[i].duration != 0:
                entries += 1
                total_sum += date_list[i].duration
        i+=1

    # If there are no entries, average will automatically equal zero to avoid trying to divide 0 by 0 
    average = total_sum/entries if entries != 0 else 0
    
    # Append the result to the averages list
    average_list.append({
        "date": format_date(date),
        "average_delivery_time": average
    })

write_results(average_list)



