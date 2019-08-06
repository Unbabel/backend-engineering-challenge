from data_format import NUMBER_PARAMS, PARAM, PARAM_TYPE, TIMESTAMP_PARAM, EVENT_PARAM, DURATION_PARAM #impor useful constants
from datetime import datetime, timedelta #used to treat datetime data

#This module contains the tools to manipulate the json objects obtained with the iojson module
#It is able to process the objects and retrieve useful parameters from them

class EventFilter():
    """" This class contains methods to filter events (json objects) from the previously read .json file"""
    
    def check_cli_compatibility(self,list_events):
        """"This method will verify if the JSON objects read are valid for the CLI

    list_events --- the array of events read from the .json file

    return a list with the filtered events, i.e., the ones suitable for the CLI"""
    
        #The first CLI compatibility filter removes every object that does not have 8 params
        filtered_events = [single_event for single_event in list_events if len(single_event) == NUMBER_PARAMS]
    
        #Then, two inner functions are defined
        #The first one checks the key compatibility of each object and ensures that they match the expected keys
        def key_compatibility(event):
            for key in event.keys():
                if key != PARAM[list(event.keys()).index(key)] :
                    return False
        
            return True
    
        #The filtered events are updated
        filtered_events[:] = filter(key_compatibility,filtered_events)
        
        #The second one checks the value type compatibility of each object and ensures that they match the expected value types
        def value_compatibility(event):
            for parameter in event.values():
                if isinstance(parameter,PARAM_TYPE[list(event.values()).index(parameter)]):
                    continue
                else:
                    return False
                
            return True
        
        #The filtered events are updated
        filtered_events[:] = filter(value_compatibility,filtered_events)
    
        #It now returns the list of events suitable for the CLI
        #calling this method ensures that no errors will come in future processing of the objects
        return filtered_events

    def filter_event_name(self,list_events,status="translation_delivered"):
       """ This method will verify if the JSON objects events correspond to deliver events.
           It is recommended to use the self.check_cli_compatibility method before, since that will prevent any error coming from unsuitable JSON objects format
           
           list_events --- the array of events 
           status --- the status to be compared (default = "translation_delivered")
           
           return a list with the filtered events, i.e., the ones corresponding to delivered translations"""
       
       #In the future, the status may change, but for now it can be used as a default argument
       #The events are filtered and the list is returned
       filtered_events = [single_event for single_event in list_events if single_event[PARAM[EVENT_PARAM]]==status]
       
       return filtered_events
    

    def get_last_events(self,list_events,time_now,time_delta):
        """ This method will retrieve the last events from an array of events, i.e., the ones that have ocurred in the last time_delta
    It is recommended to use the self.check_cli_compatibility method before, since that will prevent any error coming from unsuitable JSON objects format
    
    list_events --- the array of events
    time_now --- the start time for the comparison
    time_delta --- the delta time that delimits the time window in which the events will be retrieved
    
    return a list with the filtered events, i.e., the ones corresponding to delivered translations"""
    
        #The events in the list are first ordered by time, in a reverse order (most recent event on first index)
        #This helps the following process
        ordered_events = sorted(list_events,key=lambda x: datetime.strptime(x[PARAM[TIMESTAMP_PARAM]], '%Y-%m-%d %H:%M:%S.%f'), reverse=True)

        #null_delta is defined as a datetime '0', useful for comparison purposes
        null_delta = timedelta()
        
        #All the events are then looped to find the ones between time_now and time_delta ago
        last_events=[]
        for event in ordered_events:
            if time_now - datetime.strptime(event[PARAM[TIMESTAMP_PARAM]],'%Y-%m-%d %H:%M:%S.%f') >= null_delta:
                if time_now - datetime.strptime(event[PARAM[TIMESTAMP_PARAM]],'%Y-%m-%d %H:%M:%S.%f') <= time_delta :
                    last_events.append(event)
        
                else:        #As soon as a first event is detected to be out of the time window, we can break the cycle because the events were ordered before
                    break    #This makes the process faster if we have thousands of JSON objects to iterate
    
        #A list with the events is then retrieved
        return last_events
    
    
class EventDataProcessor():
    """" This class contains methods to process events previously filtered and retrieve parameters from them."""

    def get_num_events_per_min(self, events, start_time):
        """ This method takes an array of ORDERED events and a start time and retrieves the number of events that have ocurred between start_time and start_time - 1 minute.
    It also retrieves the indexes of the events in the array provided
    
    events --- the array of ordered events
    start_time --- start_time to start the comparison
    
    return number of events, indexes of those events in the array """
        
        #null_delta is defined as a datetime '0', useful for comparison purposes
        null_delta = timedelta()
        
        #The number of events is initially 0
        num_events = 0
        
        #list to hold the event indexes
        event_indexes = []
        for event in events:
            if start_time - datetime.strptime(event[PARAM[TIMESTAMP_PARAM]],'%Y-%m-%d %H:%M:%S.%f') >= null_delta:
                 if start_time - datetime.strptime(event[PARAM[TIMESTAMP_PARAM]],'%Y-%m-%d %H:%M:%S.%f') <= timedelta(minutes=1):
                    num_events +=1 #Each time an event is found, the number of events increments
                    event_indexes.append(events.index(event)) #And the index list is updated
                    
                 else: #As soon as an event is not in that time window, the loop can break because it is assumed that the events are ordered by time
                    break
        
        return num_events, event_indexes
            
    def compute_mov_avg_delivery_time(self, valid_events, start_time, window_size):
        """This method computes the moving average, per minute, of an array of events

    valid_events --- the array of ordered events (already filtered) to be processed
    start_time --- the start time of execution
    window_size --- the time window size, in minutes, to be processed (events between start_time and start_time - window_size)
    
    return list of moving averages, representing a moving average per minute in the time limits specified"""
        
        #The quick idea behind this algorithm is the following
        # 1) It finds the number of events in every minute window in the time limits that the user specified
        # 2) For each minute bin, if at least one event was found, the moving average is updated
        # 3) If no event was found, then the moving average is the same as the one computed in the previous bin
        

        prev_avg = 0     #initially, the mov avg is 0
        curr_avg = 0     #variable to update the current mov avg
        total_events = 0 #variable to store the total number of events
        total_dur = 0    #variable to store the total duration of the events
        mov_avg = []     #list to hold the moving averages per minute bin
        
        #null_delta is defined as a datetime '0', useful for comparison purposes
        time_null = timedelta()
        
        #time_inc is defined as the datetime increment
        time_inc = timedelta()
        
        while time_inc <= window_size: #while time is not bigger than the window_size specified
            #the num of events per minute is computed
            num_events,event_indexes=self.get_num_events_per_min(valid_events,start_time-time_inc)
            #the total num of events is updated
            total_events += num_events
            #if no events were found, the mov avg is the same as before            
            if num_events == 0:
                mov_avg.append(prev_avg)
            
            #else, we compute the moving average and append it to the list
            else:
                for index in event_indexes:
                    total_dur+=valid_events[index][PARAM[DURATION_PARAM]]
                
                curr_avg = total_dur/total_events
                mov_avg.append(curr_avg)
            
            # either way, we update the prev_avg variable with the value of curr_avg
            prev_avg = curr_avg
            
            #and we increment the cycle
            time_inc = time_inc + timedelta(minutes=1)
        
        #finnaly we retrieve the list that will always have a len equal to the number of minutes in the window_size plus 1 (corresponding to the actual start_time)
        return mov_avg
    
    def create_json_objects(self, start_time, window_size, mov_avg):
        """This method generates JSON objects in the format specified in the challenge.
           start_time --- the start time of execution
           window_size --- the window size, in minutes, specified by the user
           mov_avg --- the list of moving averages computed
           
           return a list of json objects ready to be written to a file"""
        
        #The window_size variable is converted to an actual int representing minutes
        total_minutes = int(window_size.total_seconds()/60)
        
        #A list with the dates is generated
        #Notice the range(total_minutes + 1), where the extra 1 comes from the fact that we want the start time of execution to be on the list too
        date_list = [start_time-timedelta(minutes=x) for x in range(total_minutes+1)]
        
        #Finally, the JSON objects are generated with only two parameters per object: date and average_delivery_time
        #Again, notice the range(total_minutes + 1), where the extra 1 comes from the fact that we want one json object with the start time of execution too
        json_objects = [{"date":datetime.strftime(date_list[i],'%Y-%m-%d %H:%M:%S.%f'),"average_delivery_time":mov_avg[i]} for i in range(total_minutes+1)]
        
        #A list with JSON objects is returned
        return json_objects
