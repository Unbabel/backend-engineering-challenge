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
def get_command_args():
	parser = argparse.ArgumentParser(description='Aggregate events by minutes')
	parser.add_argument('--input_file',  required=True, type=str, help='Json file name with events')
	parser.add_argument('--window_size',  required=True, type=check_int, help='Moving avg window size (in min)')
	args = parser.parse_args()
	return args

### read input data
def read_input_file(input_file: str) -> list:
	data = []
	with open(input_file) as f:
		for line in f:
			data.append(json.loads(line))
	f.close()
	return data

### calc avg for every min according to window size
def cacl_avg_delivery_time(data: pd.DataFrame, window_size: int) -> list:
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
	return result

### write output data
def write_output_file(result:dict):
	with open('outputfile.json', 'w') as f:
		for r in result:
			f.write("%s\n" % json.dumps(r))

if __name__ == '__main__':
	args = get_command_args()
	data = read_input_file(args.input_file)
	print(args)
	result = cacl_avg_delivery_time(data, args.window_size)
	write_output_file(result)