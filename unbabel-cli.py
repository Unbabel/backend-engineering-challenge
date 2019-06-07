import argparse
import json
import datetime

def main_func():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", dest="myFile", help="Open specified file")
    parser.add_argument("-w","--window_size", dest="window_size", help="Specify window size" )
    args = parser.parse_args()
    myFile = args.myFile
    window_size = args.window_size
    calculate_average(myFile, window_size)

'''
convert_timestamp() function is to accept the json data timestamp and convert it into designated timestamp
'''
def convert_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').replace(second=0,microsecond=0)
'''
outputSimulationFunction is to write to the output.json file in the format specified
'''
def outputSimulationFunction(duration, timestamp, outfile):
    output_str = ('{"Timestamp": "' + str(timestamp) + '", "Average Translation delivery time": ' + str(duration) + '}')
    outfile.write(output_str + '\n')
'''
calculate_average function is to process the input json file and determine the average delivery time for last 'X' minutes
'''
def calculate_average(myFile, window_size):
    minute_window = int(window_size)
    this_min = ""
    text = open(myFile)
    lines = text.readlines()
    current_time = 0
    average = 0.0
    first_json_stream= True
    window_time = 0
    with open("output.json", "w") as out:
        for line in lines:
            data = json.loads(line)
            iteration_ts = datetime.datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
            if first_json_stream:
                json_timestamp = data["timestamp"]
                duration = int(data["duration"])
                first_iter_ts = iteration_ts.replace(second=0, microsecond=0)
                window_time = first_iter_ts + datetime.timedelta(minutes=minute_window) # window_time is to determine the time based on user input to determine the window of the calculation
                first_json_stream = False
                outputSimulationFunction(average, first_iter_ts, outfile=out)
                current_time = first_iter_ts + datetime.timedelta(minutes=1)
                old_duration = duration
                average = old_duration
            else:
                duration = old_duration
                iteration_duration = int(data["duration"])
                while current_time < iteration_ts:
                    if current_time > window_time:
                        break
                    else:
                        outputSimulationFunction(average, current_time, outfile=out)
                    current_time = current_time + datetime.timedelta(minutes=1)
                    old_duration = iteration_duration
                average = (old_duration + duration)/2

if __name__ == "__main__":
    main_func()
