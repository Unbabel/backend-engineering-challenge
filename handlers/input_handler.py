import argparse
import datetime
import json
import os


def check_and_read_file(parser, filepath):
  """
  Parses the data form the file, validating it first
  :param parser: argument parser (python object)
  :param filepath: string with path for file
  :return:
  """

  # check if file exists
  if not os.path.exists(filepath):
    print(f"The file {filepath} does not exist!")
    return False

  # read the file line by line and assert each line is json stirng
  dates = {}
  with open(filepath) as f:
    for entry in f:
      try:
        entry = (json.loads(entry))
        dates = parse_data(entry, dates)
      except json.decoder.JSONDecodeError as execption:
        # if not a json format, return error
        print(f"The file {filepath} contains invalid data: {entry}")
        return False
  return dates


def parse_data(entry, dates):
  """
  Parses input data (json format) and stores it into a dict structure.
  The dict key is the timestamp as y:m:d h:m:00" so each bucket corresponds
  to a minute on the stream
  :param entry: json format
  :param dates: storage variable python dict
  :return: the storage variable as dict
  """
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

def filter_size(w):
  w = int(w)
  if w < 1:
    raise argparse.ArgumentTypeError("Minimum window size is 1")
  return w

def handle_input_args(argv):
  """
  hangles the input from the command line
  :param argv:
  :return:
  """
  parser = argparse.ArgumentParser(add_help=False)

  parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                      help='Command Line interface to compute (moving) average '
                           'time of a given metrics file based on a window size')

  parser.add_argument("-f", "--file", dest="input_data", required=True,
                      help="File path with translation metrics data",
                      type=lambda filepath: check_and_read_file(parser,
                                                                filepath))

  parser.add_argument("-w", "--window_size", dest="window_size", required=False,
                      help="Moving window size in minutes (should be >0)", default=10,
                      type=filter_size)

  # todo: flag True to yield word count metrics

  # parser.add_argument("-wc", "--word_count", required=False, default=False,
  #                     help="Word count flag allow to retrieve metrics such as "
  #                          "total word count and word coutn per second",
  #                     metavar="KEY")

  # todo - not the most elegant way. the client name should be passed to the
  # check and read file so data could be discarderd while reading and save
  # memory and processing time
  # parser.add_argument("-c", "--client_name", dest="client_name", required=False,
  #                     default=None, help="Filter result data by client name",
  #                     type=str)

  parser.add_argument("-o", "--output_file", dest="output_file_name",
                      required=False, default=False,
                      help="Filename to output data. If none, data will be "
                           "printed to the console", type=str)


  return parser.parse_args(argv[1:])

