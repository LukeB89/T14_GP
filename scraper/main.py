'''
Created on 10 Feb 2020

@author: Luke Byrne
'''
# Import liberies for use of the  
import time
from datetime import datetime
import requests
import json
import csv
import os.path
  

def json_parser():
    '''JSON Parser for Dublin Bikes
    
        takes no inputs and returns no output. It will create a CSV file if 
        one is not present and store results there.'''
    
#   Variable Dclarations 
    outdict = {}
    linecount = 0
    
#   code to be used when retrieving JSON file from api
    try:
        url = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4524f0f3a8f5e1b52a6de292a90ae8505b73c416'
        r = requests.get(url)
        data = r.json()
#         print("data recieved") # uncomment for debugging
    except:
        return False
#   goes through each line in the data and builds a dictionary.
#   the dictionary will store each value under the one key.  
    for line in data:
        linecount += 1
        for key in line:
            # position is a special case. position contains a dictionary as a result
            # this code extracts the "lat" and "lng" and stores them as their own 
            # key in the dictionary
            if key == "position":
                if "lat" not in outdict and "lng" not in outdict:
                    tkey = "lat"
                    outdict[tkey] = []
                    outdict[tkey].append(line[key][tkey])
                    tkey = "lng"
                    outdict[tkey] = []
                    outdict[tkey].append(line[key][tkey])
                else:
                    tkey = "lat"
                    outdict[tkey].append(line[key][tkey])
                    tkey = "lng"
                    outdict[tkey].append(line[key][tkey])
            # last_update is also a special case. this contains a time stamp that is converted
            # first 10 digits are used as the time stamp.
            elif key == "last_update":
                d = str(line[key])
                d_time = datetime.fromtimestamp(int(d[:10]))
                if key not in outdict:
                    outdict[key] = [] 
                outdict[key].append(d_time)
            elif key not in outdict:
                outdict[key] = [] 
                outdict[key].append(line[key])
            else:
                outdict[key].append(line[key])
#   checks to see if the CSV file is there. if not it will make it in the same folder as the python file.
    if os.path.isfile('bikesdata.csv'):
        pass
    else:
        with open('bikesdata.csv', 'w', newline='') as file:
            pass
    
    
    #         read from csv code, checks if first line exsits and assigns head_row
    with open('bikesdata.csv', 'r') as file:
        csvdata = csv.reader(file)
        try:
            head_row = next(csvdata)
        except:
            head_row = []

#   opens the CSV file and assigns it to appened in the writing format   
    with open('bikesdata.csv', 'a', newline='') as file:
        rowout = csv.writer(file)
        # compares the head_row to the list of keys in the dictionary
        # if all of them are there  it passes if not it creates a head row.
        # this is to ensure that an empty file will have a header row 
        if all(col in head_row for col in list(outdict.keys())):
#             print("already exsits")
            pass
        else:
#             print("creating now")
            head_row = list(outdict.keys())
            rowout.writerow(head_row)
        # this builds each of the rows with the information to be stored
        # it does this by enumerating the head_row so that it can insert the information
        # into the correct index in the row and uses the key to access the dictionary value it needs
        # the line number stored in index refers to the index in the list that is stored in the dictionary
        # index 0 refers to the first entry which in turn refers to the first line from the JSON file
        row = []
        for index in range(linecount):
            for i, key in enumerate(head_row):
                row.insert(i, outdict[key][index])            
            rowout.writerow(row)
            row.clear()
                
    return True

def main():
    
#   main code that will be run concurrently every minute
#   each loop will run the json_parser and every 60 loops will display its progress
    count = 0
    
    with open('log.txt', 'a', newline='') as file:
        log_out = csv.writer(file)
        
        while True:
            log = json_parser()
            if not log:
                log_out.writerow(["Error detected in API retrieval. Resetting"])
            if count%60 ==0:
                str_o = "Pulled {} items".format(count)
                log_out.writerow([str_o])
            time.sleep(60)
            count += 1
    return
if __name__ == '__main__':
    main()
