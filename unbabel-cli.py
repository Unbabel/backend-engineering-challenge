"""Bakckend Engineering Challenge from UNBABEL
Your mission is to build a simple command line application that parses a stream
of events and produces an aggregated output. In this case, we're instered in
calculating, for every minute, a moving average of the translation delivery
time for the last X minutes.
The input file format would be something like:
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75
aa5","source_language": "en","target_language": "fr","client_name": "easyjet",
"event_name": "translation_requested","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75
aa4","source_language": "en","target_language": "fr","client_name": "easyjet",
"event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75
bb33","source_language": "en","target_language": "fr","client_name": "booking",
"event_name": "translation_delivered","nr_words": 100, "duration": 54}
The output file should be something in the following format.
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 35,5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 58}
"""


import sys
import json
from datetime import datetime
from datetime import timedelta


def avg_delivery_time(inputfile, total_minutes):

    try:
        output_file = open("output.json", "w")
    except IOError as err:
        print("I/O error: {0}".format(err))

    try:
        with open(inputfile, "r") as fl:
            this_minute = ""
            this_minute_total = 0
            this_minute_count = 0
            lang_trend = dict()

            for line in fl:
                data = json.loads(line)  # Input itself isn't a JSON 'SEQUENCE'

                # Extra Points (I mean effort!)
                # To check which language sets have been trending
                # during given time.
                if(data["event_name"] == "translation_requested"):
                    source_target = (data["source_language"] + "-" +
                                     data["target_language"])
                    lang_trend[source_target] = (lang_trend.get(source_target,
                                                                0) + 1)

                # Skip Other Events
                if(data["event_name"] != "translation_delivered"):
                    continue

                # Determine This Minute
                this_time = datetime.strptime(
                    data["timestamp"],
                    '%Y-%m-%d %H:%M:%S.%f').replace(second=0, microsecond=0)

                # On Each New Minute
                if(this_minute != this_time):  # Time w/o seconds

                    # If not the first minute, means already the minute started
                    # then add to output
                    if(this_minute_count):
                        # exit loop if total_minutes reached
                        if(this_time >= end_minute):
                            break

                        this_minute_avg = this_minute_total/this_minute_count
                        # TODO: The average can be formatted to a given format
                        output_str = ('{"date": "' + str(this_minute) +
                                      '", "average_delivery_time": ' +
                                      str(this_minute_avg) + '}')
                        output_file.write(output_str + '\n')
                    else:
                        # Determine time limit once, in the the first minute
                        end_minute = datetime.strptime(
                            data["timestamp"], '%Y-%m-%d %H:%M:%S.%f').replace(
                                second=0,
                                microsecond=0
                                )
                        end_minute = end_minute + timedelta(
                            minutes=total_minutes+1)

                    this_minute = this_time
                    this_minute_total = data["duration"]
                    this_minute_count = 1
                else:
                    this_minute_count = this_minute_count + 1
                    this_minute_total = this_minute_total + data["duration"]

            # Following 3 statements are repeated in violation of DRY principal
            # but extracting these lines into a function, and then, calling
            # the funcion also. in the main for-loop above, will be costlier,
            # so, I think this extraction, does not worth here
            if(this_minute_count):
                this_minute_avg = this_minute_total/this_minute_count
                output_str = ('{"date": "' + str(this_minute) +
                              '", "average_delivery_time": ' +
                              str(this_minute_avg) + '}')
                output_file.write(output_str)

        if(this_minute_count):
            output_file.write('\n\nLanguage set requested during this time:\n')

            for k, v in lang_trend.items():
                output_file.write("\n" + k.encode('ascii') + " = " + str(v))
        else:
            output_file.write('No Input Data!!')

        output_file.close()

    except IOError as err:
        print("I/O error: {0}".format(err))
    except:
        print("Got errors!")

    if(this_minute_count):
        # Most Popular Lang-Sets
        sorted_trend = sorted(lang_trend, key=lambda x: (-lang_trend[x], x))

        print("\nTrending Language Sets:")
        for lang_set in sorted_trend[0:3]:
            print(lang_set)

        print("\nDetailed output in output.json, updated!")
    else:
        print("No Input Data!!")

if __name__ == "__main__":
    import sys
    # TODO: input file can be checked here also for any I/O error
    # TODO: Number of total_minutes can be checked here, to cut it to size

    # total_minutes (size) input should be a positive integer greater than 0
    try:
        val = int(sys.argv[2])
        if(val > 0):
            import time
            start = time.time()
            avg_delivery_time(str(sys.argv[1]), int(sys.argv[2]))
            end = time.time()
            print("Executed in:", end - start)
        else:
            raise ValueError

    except ValueError:
        print("Please provide the second argument as valid number of minutes")
    except IndexError:
        print("Please provide input filename, followed by number of minutes")
