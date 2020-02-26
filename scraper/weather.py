"""
Created on 11 Feb 2020
@author: Milo Bashford
"""

import requests
import json
import time
from datetime import datetime


def get_weather_data(**kwargs):
    """gets live weather data from openweathermap.org.
    Takes keyword args 'lat' & 'lon' (ie. latitude and longitude):
    default values of'lat' & 'lon' return weather for Dublin city.
    Returns a dictionary containing weather data"""

    if "lat" in kwargs:
        lat = kwargs["lat"]
    else:
        lat = 53.3498                                   # Dublin latitude
    if "lon" in kwargs:
        lon = kwargs["lon"]
    else:
        lon = -6.2603                                   # Dublin longitude
    if "key" in kwargs:
        key = kwargs["key"]
    else:
        key = "86baa129046e5cbaeb16af074356e579"        # default openWeatherMap API key

    # create openWeatherMap API query using input latitude, longitude and api key
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + key
    print(url)

    # get weather info and convert to python dict
    response = requests.get(url)
    temp_dict = json.loads(response.text)

    if "weather" in temp_dict:
        temp_dict["weather"] = temp_dict["weather"][0]

    # stores data to be returned
    out_dict = {}
    """
    # rename duplicate keys & remove redundant list (@ outdict["weather"][0])
    for key in temp_dict:
        if key == "weather":
            out_dict[key] = temp_dict[key][0]
            out_dict[key]["weather_id"] = temp_dict["weather"]["id"]
    if "rain" in temp_dict:
        out_dict["rain"]["precipitation_chance"] = temp_dict["rain"]["1h"]
    out_dict["sys"]["system_id"] = outtemp_dict["sys"]["id"]
    """
    return temp_dict


def flatten_dict(some_dict):
    """Takes a parent dictionary containing multiple nested dictionaries and returns a
    single non-nested dictionary combining all keys from the root dictionary with all
    keys contained in nested dictionaries. Duplicate keys must be renamed prior to calling
    this function otherwise it will overwrite data!! This is a recursive function!!"""

    outdict = {}                                            # init empty dict to hold output

    keys = list(some_dict.keys())

    for i in keys:

        if type(some_dict[i]) == dict:                      # if key is nested dict; call flatten_dict(key)
            some_dict[i] = prefix_keys(some_dict[i], i)
            outdict.update(flatten_dict(some_dict[i]))

        elif type(some_dict[i]) == list:                    # else if key is nested list; call flatten_dict(key)
            for j in some_dict[i]:
                outdict.update(flatten_dict(j))

        else:                                               # else; copy key-value to output dict
            outdict[i] = some_dict.pop(i)

    return outdict


def prefix_keys(some_dict, prefix):
    """returns a dictionary with a prefix to the name of each key in the top level of the dictionary"""

    keys = list(some_dict.keys())
    temp_dict = {}
    for key in keys:
        temp_dict[prefix + "_" + key] = some_dict.pop(key)
        some_dict.update(temp_dict)
    return some_dict


def get_weather():
    """Test Loop"""
    count = 0
    while count < 3:
        x = get_weather_data()

        y = flatten_dict(x)

        # open weather data updated one every 10 minutes

        with open("temp.txt", "a") as file:
            file.write(json.dumps(y))

        count += 1
        time.sleep(600)
