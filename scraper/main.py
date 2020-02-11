'''
Created on 10 Feb 2020

@author: Luke Byrne
'''
import time
from datetime import datetime
import requests
import json
import csv
import os.path
  


def json_parser():
    outdict = {}
    linecount = 0
#     code to be used when retrieving JSON file from api
    url = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4524f0f3a8f5e1b52a6de292a90ae8505b73c416'
    r = requests.get(url)
    data = r.json()
#     print("data recieved")

    
#     data will be replaced with above json to iliminate need for JSON file
#     with open('data.txt') as json_file:
#     data = json.load(json_file)
    for line in data:
        linecount += 1
        for key in line:
            
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

    if os.path.isfile('bikesdata.csv'):
        pass
    else:
        with open('bikesdata.csv', 'w', newline='') as file:
            pass
    
    
    #         read from csv code, checks if first line exsits and assigns row 1
    
    with open('bikesdata.csv', 'r') as file:
        csvdata = csv.reader(file)
        try:
            head_row = next(csvdata)
        except:
            head_row = []

        
        
    with open('bikesdata.csv', 'a', newline='') as file:
        rowout = csv.writer(file)
        
        if all(col in head_row for col in list(outdict.keys())):
#             print("already exsits")
            pass
        else:
#             print("creating now")
            head_row = list(outdict.keys())
            rowout.writerow(head_row)
        
        row = []
        for index in range(linecount):
            for i, key in enumerate(head_row):
                row.insert(i, outdict[key][index])            
            rowout.writerow(row)
            row.clear()
                
    return

def main():
    
#     main code that will be run concurrently every minuete
#     too be filled at a later date just getting the base working now
    count = 0
    while True:
        json_parser()
        if count%60 ==0:
            print("Pulled {} items".format(count))
        time.sleep(60)
        count += 1
    return
if __name__ == '__main__':
    main()
