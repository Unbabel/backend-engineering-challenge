#The idea behind this module is to implement several constants associated with the expected json objects format to be read in the CLI
#It also helps any future change in the program, specially in the manipulator module, case one day the format of the json objects change
#If that is the case, chances are only this module needs to be changed

NUMBER_PARAMS = 8 #The number of params each json object must have

#The index of each param
TIMESTAMP_PARAM = 0
ID_PARAM = 1
SOURCE_PARAM = 2
TARGET_PARAM = 3
CLIENT_PARAM = 4
EVENT_PARAM = 5
WORD_PARAM = 6
DURATION_PARAM = 7

#The key of each param
PARAM = ("timestamp",
          "translation_id",
          "source_language",
          "target_language",
          "client_name",
          "event_name",
          "nr_words",
          "duration")

#The type of each param
PARAM_TYPE = (str,
              str,
              str,
              str,
              str,
              str,
              int,
              int)

