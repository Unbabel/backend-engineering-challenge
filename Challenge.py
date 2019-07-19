import datetime
import json
from statistics import mean


#reproducing an INPUT in form of a list, with just 2 keys, because we don't need other keys to solve the (basic) challenge
x1={
	"timestamp":"2018-12-11 18:11:08.56",
	"duration":20
        }
x2={
	"timestamp":"2018-12-11 18:15:19.90",
	"duration":31}
x3={
	"timestamp":"2018-12-11 18:23:19.90",
	"duration":54}   
        
INPUTFILE=[x1,x2,x3] #assuming input file as a list of dictionaries sorted by the key "datetime" format 

def addDateTime(INPUTFILE):         #convert string values in datetime format, and add this key to each dictionaries
    for ev in INPUTFILE:
        ev["datetime"]=datetime.datetime(
		int(ev["timestamp"][0:4]),
		int(ev["timestamp"][5:7]),
		int(ev["timestamp"][8:10]),
		int(ev["timestamp"][11:13]),
		int(ev["timestamp"][14:16]),
		int(ev["timestamp"][17:19]))
      
        
def challenge(INPUTFILE,intervaltime):      #intervaltime is representing the interval (in minutes) on wich we'll calculate the average
	nt=datetime.timedelta()             #timedelta=0, nedeed for conforntation
	onemin=datetime.timedelta(minutes=1) #the delta that will be progressively add to the "starting time"
	INT=datetime.timedelta(minutes=intervaltime)
	st=INPUTFILE[0]["datetime"].replace(second=0,microsecond=0)  #replaces the first element of the input file in XX:XX:00.000000 format, defining the starting time
	et=INPUTFILE[-1]["datetime"].replace(second=0,microsecond=0) #replaces the last element of the input file in XX:XX:00.000000 format, define the starting time (-1 min)
	et=et+onemin #ending time
	DIZ=  []                                                #Initialize a new list where the output dictionaries will be stored 
	while(st<=et):                                      #iteration valid until is not reached the ending time
		l=[]                                        #initialize a list object to perform the mean
		for ev in INPUTFILE:
			if (nt<=st-ev["datetime"]) and (st-INT<=ev["datetime"]): # for each evaluation from the input file,  verify that it's not above the interval time and include it in a list.If is above, refresh the list with the next values.
				l=l+[ev["du"]]
			if l==[]: m=0       #solving the problem that "mean" in statistics module can't perform on empty list
			else: m=mean(l)  #perform the aritmetic average in the list
			diz={
			"date":st.strftime("%Y-%m-%d %H:%M:%S"), #return the datetime object into a string
			"average_delivery_time":m} #return the average
		DIZ=DIZ+[diz]  #update the output list
		st=st+onemin #increase the starting time of one minute
	app_json=json.dumps(DIZ) #convert the dictionary obtained into a json
	print(app_json)
    

    

    
    
