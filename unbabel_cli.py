import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime, timedelta

### get command line args
input_file = 'events.json'
window_size = 10
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




### write output data