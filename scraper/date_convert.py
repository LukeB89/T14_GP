"""
Created on 09 March 2020
@author: Luke Byrne

method to convert datetime formats into timestamp on the database
"""
import time
from datetime import datetime as dt
import json
import db_interactions as db

with open('bikesdata.json', 'r', newline='') as file:
    data = json.load(file)

for line in data:
    keys_dict = {"number":0, "last_update":0}
    data_dict = {"last_update":0}
    for key in line:
 
        if key == "last_update":
            if '/' in line[key]:
                keys_dict[key] = line[key]
                data_dict[key] = int(dt.timestamp(dt.strptime(line[key], '%d/%m/%Y %H:%M')))
            elif '-' in line[key]:
                keys_dict[key] = line[key]
                data_dict[key] = int(dt.timestamp(dt.strptime(line[key], '%Y-%m-%d %H:%M:%S')))
            else:
                pass
        elif key == "number":
            keys_dict[key] = line[key]
        else:
            pass
    
    print("keys: ", keys_dict)
    print("data: ", data_dict)
    db.db_query(query='update', table='dynamic', data=data_dict, pkeys=keys_dict)
