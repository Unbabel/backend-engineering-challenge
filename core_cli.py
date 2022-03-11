import datetime
import sys
from handlers.input_handler import handle_input_args #, INCLUDE_WC

TOLERANCE = 2

def compute_moving_average(data, window_size):
  """
  Computes a moving average over the collected data.
  Each key in the data dict is a unique minute. For each minute, sums the
  total duration and counts how many translations were performed
  on the previous 10 min.
  Note that the calculation is not done over the last 10 samples, but the last
  10 (efective time) minutes
  :param data: python dict with processed data
  :param window_size: window size for moving average
  :return: input data dict with extra attribute for each minute (Avg)
  """
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
  """
  Yields the information to the user.  If the file name is present, it writes
  to the file, otherwise it prints to the command line
  :param data: python dict containing processed information
  :param output_file_name: destination file name or None
  :return:
  """
  if output_file_name:
    with open(output_file_name, 'w') as f:
      [f.write(str({"date": d.strftime("%Y-%m-%d %H:%M:%S"),
                    "average_delivery_time": data[d]["avg"]}) + "\n") for d in
       data]
  else:
    [print(str({"date": d.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": data[d]["avg"]})) for d in data]

# todo
# def filter_by_client(data, client_name):
#   """
#   Allows to create a subset of data that matches the client name
#   Important Note: This is not the most elegant way of doing it.
#   The client name should be passed to the check and read file so data could
#   be discarderd while reading and save memory and processing time
#   :param client_name: string
#   :return: python dict containing filtered data
#   """
#   for instant in list(data.keys()):
#     if data[instant]['client_name'] != client_name:
#       del data[instant]
#   return data

def process(argvs):
  """
  Main function that processes the information
  :param argvs: arguments from command line
  :return: calls the method that outputs data to the user
  """
  bulk_data = handle_input_args(argvs)
  data_dict = bulk_data.input_data
  window_size = bulk_data.window_size
  output_file_name = bulk_data.output_file_name
  # todo
  # if bulk_data.client_name:
  #   data_dict = filter_by_client(data_dict, bulk_data.client_name)
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
