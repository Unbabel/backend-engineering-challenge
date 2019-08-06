import json #used to encode/decode json data
import re   #used to aid in any necessary identation correction to the input json data

REMOVE_WHITESPACE = re.compile(r'[^\s]')

#This module will simply deal with the JSON Inputs and Outputs.
#It can read arbitrary .json files and write arbitrary .json files with the format shown on the challenge

def read_json_file(filename):
    """This function attemps to decode a .json file.
    If sucessful, it returns a list with the objects.
    If it fails, returns None.
    
    filename -- the name of the .json file
    
    Note: the function will fail if the file does not exist or if the JSON syntax is incorrect, for example."""
    
    #The function will TRY to read the specified file
    #The with operator is used to ensure that the file is closed in the presence of some exception
    try:
        with open(filename,'r') as file:
            raw_data = file.read()
        
    #In case an exception is raised, e.g., the file does not exist, the function returns None
    except:
        print("The specified file: \'" + filename + "\' does not exist.")
        return None
        
    #Otherwise, the function continues
    else:
        
        #If the function reaches this stage, at least the file exists, so a special nested generator called decode_file is first defined
        #This generator will iterate over the .json file and yield an object in each iteration
        #Not only that, but the generator is also able to read from whatever .json format, including an ugly one with whitespaces,
        #provided that the correct .json syntax is respected. This does not limit the CLI to the specific format introduced in the challenge scenario
        
        def decode_file(raw_data):
            decoder = json.JSONDecoder() #json decoder
            pos = 0 #starts at the beginning of the .json file
            
            while True:
                match = REMOVE_WHITESPACE.search(raw_data, pos) #checks for a whitespace
                
                if not match: #if no whitespace was found, just go back and try again
                    return
            
                pos = match.start() #but if a match was found, save that position first
            
                try:
                    event, pos = decoder.raw_decode(raw_data, pos) #try to raw decode the data so far
                
                except json.JSONDecodeError as err: #if this exception occurs it is because the .json syntax is wrong
                    yield (None, err) #yield a tuple with no json object read and an error, so that the exception can be handled outside the generator
            
                else:
                    yield (event,None) #or if no exception occurs, then yield the object, you have no error, please continue
    
        events=decode_file(raw_data) #Lets try to run the generator (again)
        
        list_events=[]
        for event, error in events:
            #If the error ocurred, then inform the user and return None
            if error:
                print("Invalid JSON syntax in the provided file: \'" + filename + "\'.")
                return None
            
            #Else, continue to append the events read from the file to a list, untill no more iterations exist in the generator and then return the list
            else:
                list_events.append(event)
        
    return list_events

def write_json_file(filename, json_objects):
    """This function attemps to encode a .json file in the format specified in the challenge.

    filename -- the name of the .json file
    json_objects -- array with the json objects to be written"""
    
    try:
        with open(filename,'w+') as file:
            for obj in json_objects:
                json_str = json.dumps(obj)
                file.write(json_str+'\n')
    
    except:
        print("The specified file: \'" + filename + "\' could not be written to.")
    


    

    

    
    
    
    
    


        
