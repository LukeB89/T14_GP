"""
Created on 18 Feb 2020
Version: 0.1.01
@author: Luke Byrne

methods for retrieving and parsing information from the Dublin bikes station
"""

import db_interactions as db
import time
from datetime import datetime
import requests
import json
import csv
import os.path
import traceback
import timeit as t
from configparser import ConfigParser

# read DataBase info from the config file
config = ConfigParser()
config.read("config.ini")
options = config["bikesAPI"]


def parse_bikes_data():
    '''JSON Parser for Dublin Bikes
    
        takes no inputs and returns no output. It will create a CSV file if 
        one is not present and store results there.'''
    
#   Variable Declarations
    dynamic_dict = dict.fromkeys(["number", "last_update", "bike_stands", "available_bike_stands", "available_bikes", "status"], None)
    static_dict = dict.fromkeys(["number", "contract_name", "name", "address", "lat", "lng", "banking", "bonus"], None)
    linecount = 0
    
#   code to be used when retrieving JSON file from api
    try:
        url = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=' + options["key"]
        r = requests.get(url)
        data = r.json()
    except:
        print(traceback.format_exc())
        return False
#   goes through each line in the data and builds a dictionary.
#   the dictionary will store each value under the one key.  
    if "error" in data:
        print("Error: {}".format(data["error"]))
        return False
    for line in data:
        
        for key in line:
            # position is a special case. position contains a dictionary as a result
            # this code extracts the "lat" and "lng" and stores them as their own 
            # key in the dictionary    
            if key == "position":
                tkey = "lat"
                static_dict[tkey] = line[key][tkey]
                tkey = "lng"
                static_dict[tkey] = line[key][tkey]
            elif key in dynamic_dict:
                dynamic_dict[key] = line[key]
            elif key in static_dict:
                static_dict[key] = line[key]
            else:
                print("{} not vaild data".format(key))
        
        print(dynamic_dict)
        db.db_query(query='push', table='dynamic', data=dynamic_dict)

        # update dynamic information held for bikes in table "bikes_dynamic": attempts
        # to "insert" information as new row, calls "update" query on duplicate key error
        response = db.db_query(query="push", table="current", data=dynamic_dict)
        if response is not None:
            # if the response is a duplicate key error perform an "update" query:
            if response[0] == 1062:
                db.db_query(query="update", table="current",
                            data=dynamic_dict, pkeys={"number": dynamic_dict["number"]})
       
    return True


