import argparse
import datetime
import json
import os


def check_and_read_file(parser, filepath):
  # check if file exists
  if not os.path.exists(filepath):
    print(f"The file {filepath} does not exist!")
    return False

  # if the file exists, read it!
  dates = {}
  with open(filepath) as f:
    for entry in f:
      try:
        entry = (json.loads(entry))
        dates = parse_data(entry, dates)
      except json.decoder.JSONDecodeError as execption:
        print(f"The file {filepath} contains invalid data: {entry}")
        return False
  return dates


def parse_data(entry, dates):
  date_ = datetime.datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
  date = date_.replace(second=0, microsecond=0)
  word_count = entry["nr_words"]
  duration = entry["duration"]
  count = 1  # the counter increases by one register for this minute
  if date in dates.keys():
    dates[date]["count"] += count
    dates[date]["word_count"] += word_count
    dates[date]["duration"] += duration
  else:
    dates[date] = {"count": count, "duration": duration,
                   "word_count": word_count}
  return dates


def handle_input_args(argv):
  parser = argparse.ArgumentParser(add_help=False)

  parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                      help='Command Line interface to compute (moving) average '
                           'time of a given metrics file based on a window size')

  parser.add_argument("-f", "--file", dest="input_data", required=True,
                      help="File path with translation metrics data",
                      type=lambda filepath: check_and_read_file(parser,
                                                                filepath))

  parser.add_argument("-w", "--window_size", dest="window_size", required=False,
                      help="Moving window size in minutes", default=10,
                      type=int)

  parser.add_argument("-o", "--output_file", dest="output_file_name",
                      required=False, default=False,
                      help="Filename to output data. If none, data will be "
                           "printed to the console", type=str)

  # parser.add_argument("-c", "--client", dest="client", required=False,
  #                     help="Will only calculate the average translation duration for the inputed client name",
  #                     type=str)

  return parser.parse_args(argv[1:])
