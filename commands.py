import argparse  #used to parse arguments
import os        #used to know the current directory
from datetime import datetime, timedelta #used to process arguments into datetime data

#In order to make the overall program more beautifull and to hide the ugly argparse methods from the main, they were compacted into the Arguments class
#This class also contains methods for the manipulation of some of these inputs
#It is also a nice strategy to group all the argparse code in a separate module in order to locate the argparse errors a little bit easier

class Arguments():
    
    """ This class parses the arguments from the command line and processes them.
        It is also responsible for saving the start time of execution of the script."""
    
    #This is starting time of execution of the script
    #It is probably the most important variable of the program together with the moving average, so it is stored as a private variable of the class
    __begin_time = datetime.now()

    #The constructor will simple add the possible arguments that can be passed through the command line and will parse them in the end
    def __init__(self):
    
        parser = argparse.ArgumentParser()
        
        #An option to specify the input file, which is always required
        parser.add_argument("-i", "--input_file", help="specify the input file to be read", action = "store_true", required = True)
        
        #The positional argument that will (hopefully) contain the name of the input .json file
        parser.add_argument("input", type = str, help="the .json input file name")
        
        #An always required option to specify the window size
        parser.add_argument("-w", "--window_size", help="specify the time window to be computed", action = "store_true", required = True)
        
        #The positional argument for the window
        parser.add_argument("window", type = int, help="the time window width in minutes")
        
        #And the arguments are parsed, hopefully with the mandatory syntax
        self.args = parser.parse_args()
        
    #This function will simply process the time parameters, i.e., it takes the time window that the user has set and converts it to more useful datetime variables
    def compute_time_args(self):
        self.time_delta = timedelta(minutes = 1)
        self.time_window = timedelta(minutes = self.args.window)
    
    #This function will simply evaluate what is going to be the output file name
    def compute_output_filename(self):
        
        #It creates a directory to store the output files
        if not os.path.exists(os.getcwd() + "/output_files"):
            os.makedirs(os.getcwd() + "/output_files")
        
        #The name of the output file is also generated from the concatenation of the output directory plus the start time of execution
        #Seems like a good solution for undecided users, since this will lower the chances of overriding files
        #If I had more time, I would probably also implement an option for the user to select an output file name if wanted (not mandatory)
        #However this seems nothing but a detail as of now
        self.output_file_name = os.getcwd() + "/output_files" + "/" + self.__begin_time.strftime("%Y-%m-%d-%H-%M-%S") + ".json"
            
    #This is not very pythonic, I'm aware, but I really wanted to protect the begin time of execution. It is a simple get function
    def get_begin_time(self):
        return self.__begin_time
             
    