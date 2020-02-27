"""
Created on 11 Feb 2020
@author: Milo Bashford
"""

import requests
import json
from db_interactions import db_query


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

    # get weather info and convert to python dict
    response = requests.get(url)
    temp_dict = json.loads(response.text)

    # remove redundant list (@ temp_dict["weather"][0])
    if "weather" in temp_dict:
        temp_dict["weather"] = temp_dict["weather"][0]

    return temp_dict


def flatten_dict(some_dict):
    """Takes a parent dictionary containing multiple nested dictionaries and returns a
    single non-nested dictionary combining all keys from the root dictionary with all
    keys contained in nested dictionaries. Duplicate keys must be renamed prior to calling
    this function otherwise it will overwrite data!! This is a recursive function!!"""

    out_dict = {}                                            # init empty dict to hold output

    keys = list(some_dict.keys())

    for i in keys:

        if type(some_dict[i]) == dict:                      # if key is nested dict; call flatten_dict(key)
            some_dict[i] = prefix_keys(some_dict[i], i)
            out_dict.update(flatten_dict(some_dict[i]))

        elif type(some_dict[i]) == list:                    # else if key is nested list; call flatten_dict(key)
            for j in some_dict[i]:
                out_dict.update(flatten_dict(j))

        else:                                               # else; copy key-value to output dict
            out_dict[i] = some_dict.pop(i)

    return out_dict


def prefix_keys(some_dict, prefix):
    """returns a dictionary with a prefix to the name of each key in the top level of the dictionary"""

    keys = list(some_dict.keys())
    temp_dict = {}
    for key in keys:
        temp_dict[prefix + "_" + key] = some_dict.pop(key)
        some_dict.update(temp_dict)
    return some_dict


def get_weather_all():
    """updates dynamic weather data for each weather station
    listed in the "weather_static" table on the RDS database"""

    # get weather station data from database table "weather_static"
    weather_stations = db_query(query="pull", table="w_static")

    # get the weather data for each weather station in the "weather_static"
    # table and push to database "weather_dynamic" table
    for station in weather_stations:
        weather_data = flatten_dict(get_weather_data(lat=station["latitude"], lon=station["longitude"]))
        # remove static data from weather_data(except for key)
        weather_data.pop("coord_lat")
        weather_data.pop("coord_lon")
        weather_data.pop("base")
        weather_data.pop("sys_type")
        weather_data.pop("sys_id")
        weather_data.pop("sys_country")
        weather_data.pop("timezone")
        weather_data.pop("id")
        weather_data.pop("cod")
        db_query(query="push", table="w_dynamic", data=weather_data)
