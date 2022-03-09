import datetime
import sys

from handlers.input_handler import handle_input_args

TOLERANCE = 2


def compute_moving_average(data, window_size):
  one_minute = datetime.timedelta(minutes=1)
  p = float(10 ** TOLERANCE)
  for time in data:
    total_counts = 0
    total_ms = 0
    for delta in range(1, window_size + 1):
      try:
        prev = time - one_minute * delta
        total_counts += data[prev]['count']
        total_ms += data[prev]['duration']
      except Exception as e:
        pass
    avg = total_ms / total_counts if total_counts > 0 and total_ms > 0 else 0
    data[time]['avg'] = int(avg * p + 0.5) / p
  return data


def output_results(data, output_file_name):
  if output_file_name:
    with open(output_file_name, 'w') as f:
      [f.write(str({"date": d.strftime("%Y-%m-%d %H:%M:%S"),
                    "average_delivery_time": data[d]["avg"]}) + "\n") for d in
       data]
  else:
    [print(str({"date": d.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": data[d]["avg"]})) for d in data]


def process(argvs):
  bulk_data = handle_input_args(argvs)
  data_dict = bulk_data.input_data
  window_size = bulk_data.window_size
  output_file_name = bulk_data.output_file_name
  processed_data = compute_moving_average(data_dict, window_size)
  return output_results(processed_data, output_file_name)


if __name__ == '__main__':
  process(sys.argv)


def run():
  try:
    process(sys.argv)
  except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(0)
