import iojson as json  #used to read / write json files
from manipulator import EventFilter, EventDataProcessor #used to manipulate the json objects
from datetime import datetime, timedelta  #used to process datetime data
from commands import Arguments #used to parse command line arguments

#This module contains the main function of the program
#This solution is written in python(python3) which seemed to be the quickest and simplest way of producing a solution given the available time I had for the project

def main():
    
    #First, an instance of the Arguments() class is created
    #It will automatically parse the command line arguments
    arguments = Arguments()
    
    #If the window size is negative, it will produce an error.
    #There is no problem in the window size being 0, since the actual start of execution time will also be outputed to a file, but no mov avg will be computed
    if arguments.args.window < 0:
        print("The time window can not be negative. This script does not predict the future.")
        return
    
    #Also, the arguments object will compute the window size that the user intends and the output filename. Both these parameters are processed from the command line arguments
    arguments.compute_time_args()
    arguments.compute_output_filename()
    
    #Then the input file is read
    list_events = json.read_json_file(arguments.args.input)
    
    #Since the previous function returns None if the json syntax is incorrect or if the file does not exist, the program ends if that is the case
    if not list_events:
        print("No events were read from the provided \'" + arguments.args.input + "\' file.")
        return
    
    #Next, we start filtering the events
    event_filter = EventFilter()
    
    #All the filtering functions described in the manipulator module are executed
    filtered_events = event_filter.check_cli_compatibility(list_events)
    filtered_events = event_filter.filter_event_name(filtered_events)
    filtered_events = event_filter.get_last_events(filtered_events,arguments.get_begin_time(),arguments.time_window)
    
    #In the end, if the list is empty, there is no point in continuing
    #The user must change the arguments, there are no JSON objects here
    if not filtered_events:
        print("No valid events were read from the provided \'" + arguments.args.input + "\' file.")
        return
    
    #Otherwise, the list is first converted to a tuple
    #This will make iterations faster which could be a must if we are dealing with large ammounts of JSON objects
    valid_events = (*filtered_events, )
    
    #Then, the moving average is processed with the methods described in the manipulator module
    #After it, the list of json objects to be written to the file is created
    event_processor = EventDataProcessor()
    mov_avg = event_processor.compute_mov_avg_delivery_time(valid_events, arguments.get_begin_time(), arguments.time_window)
    json_objects = event_processor.create_json_objects(arguments.get_begin_time(), arguments.time_window, mov_avg)
    
    #And it is attempted to write to the file
    json.write_json_file(arguments.output_file_name,json_objects)
    
    #Just an happy message for the user to know that today was a good day
    print("Program executed sucessfully!")

if __name__ == '__main__':
    main()
    
    


