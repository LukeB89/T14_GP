"""
Created on 15 Feb 2020
@author: Milo Bashford

updates the static information for weather stations associated
with individual bike stations stored on the RDS database
"""

import time


from weather import get_weather_data
from weather import flatten_dict
from db_interactions import db_query


def get_weather_stations():
    """updates the static information for weather stations associated with individual bike stations"""

    # request all bike station info from the bikes_static table and store station ID, latitude and longitude
    rows = db_query(query="pull", table="static")

    for row in rows:
        print("updating weather station data for", row["name"])
        request = flatten_dict(get_weather_data(lat=row["lat"], lon=row["lng"]))

        # update "weather_static" table with station information
        w_static_info = {"w_station_name": request["name"],
                         "latitude": request["coord_lat"],
                         "longitude": request["coord_lon"]}

        db_query(query="push", table="w_static", data=w_static_info)

        # update "bike_weather_assoc table
        assoc_info = {"bike_station_id": row["number"], "weather_station": request["name"]}
        try:
            db_query(query="push", table="assoc", data=assoc_info)
        except:
            db_query(query="update", table="assoc", data=assoc_info)
            print("attempting to update row")

        # sleep between every loop to avoid overloading the weather data api (60 request per min limit)
        time.sleep(1)

    print("Done!")


get_weather_stations()