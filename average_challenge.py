import jsonlines
import argparse
import json
from collections import deque
import datetime
import uuid


def do_main():
    parser = argparse.ArgumentParser(description='Unbabel translation metrics stream parsing CLI.')
    parser.add_argument('--input_file', type=open_file)
    parser.add_argument('--window_size', type=int)
    name_new_file = "%s.json" %  str(uuid.uuid4().hex)
    args = parser.parse_args()

    json_opened = jsonlines.Reader(args.input_file)
    
    find_average(json_opened, args.window_size, name_new_file)
    print('congrats the new file %s was generated with sucess' % name_new_file)
    
def open_file(f):
    return open(f)

def find_average(json_opened, size, name_new_file):
    first_iteration = True
    current_avg = 0.0
    current_timestamp = None

    deq = deque()
    f= open(name_new_file,"w+")
    for it_json in json_opened:
        iteration_timestamp = timestamp_to_datetime(it_json['timestamp'])
        if first_iteration:
            current_timestamp = datetime.datetime(iteration_timestamp.year, iteration_timestamp.month, iteration_timestamp.day, iteration_timestamp.hour, iteration_timestamp.minute, 0)

            first_iteration = False
            write_json_average(current_timestamp, current_avg, f)

            current_timestamp += datetime.timedelta(minutes=1)

        else:
            while current_timestamp < iteration_timestamp:
                while deq and timestamp_to_datetime(deq[0]['timestamp']) < (current_timestamp - datetime.timedelta(minutes=size)):
                    evt = deq.popleft()
                    if deq:
                        current_avg -= (evt['duration'] - current_avg)/len(deq)
                    else:
                        current_avg = 0

                write_json_average(current_timestamp, current_avg, f)
                current_timestamp += datetime.timedelta(minutes=1)

        deq.append(it_json)
        current_avg += (it_json['duration'] - current_avg)/len(deq)

    write_json_average(current_timestamp, current_avg, f)


def timestamp_to_datetime(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

def write_json_average(date, average, f):
    f.write("%s\r\n" % 
        json.dumps(
            {'date': date.strftime('%Y-%m-%d %H:%M:%S'), 'average_delivery_time': average}))


if __name__ == "__main__":
    do_main()