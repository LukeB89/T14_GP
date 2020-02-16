"""
Created on 15 Feb 2020
@author: Milo Bashford

writes a csv file containing location & id details for the weather station
associated with each dublin bikes station.
"""

import csv
import time

from weather import get_weather_data
from weather import flatten_dict

# read "bikesdata.csv" and make dict with lat, lng, name & number for each unique bikestation

with open("bikesdata.csv", newline="") as infile:
    outdict = {}
    infile = csv.DictReader(infile)
    for row in infile:
        outdict[row["name"]] = {"number": row["number"], "lat": row["lat"], "lon": row["lng"]}


print(len(outdict))

# get weather data for each bike station in dict
weather_data = {}

for station in outdict:
    request = flatten_dict(get_weather_data(lat=outdict[station]["lat"], lon=outdict[station]["lon"]))
    weather_data[station] = {"bike_station": station, "lat": request["lat"], "lon": request["lon"],
                             "w_station": request["name"], "id": request["system_id"]}

    # sleep between every loop to avoid over pining the weather data api
    time.sleep(1)

print(weather_data)
csv_columns = ["bike_station", "lat", "lon", "w_station", "id"]

with open("stations_data.csv", "w", newline="") as file:
    fileout = csv.DictWriter(file, fieldnames=csv_columns)
    fileout.writeheader()
    for row in weather_data:
        fileout.writerow(weather_data[row])
