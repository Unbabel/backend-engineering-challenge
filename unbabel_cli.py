import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
import argparse

## check if window_size is a valid integer
def check_int(value):
	ivalue = int(value)
	if ivalue <= 0:
		raise argparse.ArgumentTypeError("%s should be a integer a grater than 0" % value)
	return ivalue


### get command line args
parser = argparse.ArgumentParser(description='Aggregate events by minutes')
parser.add_argument('--input_file',  required=True, type=str, help='Json file name with events')
parser.add_argument('--window_size',  required=True, type=check_int, help='Moving avg window size (in min)')
args = parser.parse_args()
print(args.window_size)


input_file = args.input_file
window_size = args.window_size
### read input data
data = []
with open(input_file) as f:
	for line in f:
		data.append(json.loads(line))
f.close()


### calc avg for every min according to window size

#### transform in dataframe
df = json_normalize(data)
#### convert to timestamp
df["timestamp"]  = pd.to_datetime(df["timestamp"],format='%Y-%m-%d %H:%M:%S')
#### define the start and end data
ref = df["timestamp"].min().floor(freq = 'T')
end = df["timestamp"].max().ceil(freq = 'T')
#### generate data
result = []
while ref <= end:
	past = ref - timedelta(minutes = window_size)
	df_window = df[(df["timestamp"] <= ref) & (df["timestamp"] >= past)]
	avg = df_window["duration"].mean() if len(df_window) > 0 else 0
	result.append({"date":str(ref), "average_delivery_time":avg})
	ref += timedelta(minutes = 1)


print(result)

### write output data
with open('outputfile.json', 'w') as f:
	for r in result:
		f.write("%s\n" % json.dumps(r))
