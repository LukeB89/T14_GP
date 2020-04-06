"""
Created on 06 Mar 2020
Version: 0.1.01
@author: Luke Byrne

Methods for predicting and updating hourly prediction tables in the database
"""
# Set up libraries
import pandas as pd
import numpy as np
import pickle
# from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
from configparser import ConfigParser
from datetime import datetime

 # Configure the connection
config = ConfigParser()
config.read("config.ini")
options = config["DataBase"]
engine = create_engine("mysql://" + options["user"] + ":" + options["passwd"] + "@" + options["host"] + "/" + options["database"])
    
def bikesPredict(station):
    # configure day and hour
    date_now = datetime.now()
    day = date_now.weekday()  
    hour = date_now.hour+1
    day_bin = '{0:03b}'.format(day)
    hour_bin = '{0:05b}'.format(hour)
    # import the model to be used
    with open('models/dBikePredictNoCov_station_{}.pkl'.format(station), 'rb') as handle:
        noCovModel = pickle.load(handle)
    with open('models/dBikePredictCovData_station_{}.pkl'.format(station), 'rb') as handle:
        covModel = pickle.load(handle)
    with engine.connect() as conn:
        weather_data = "SELECT wc.weather_id, wc.main_temp, wc.main_humidity, wc.wind_speed FROM dublinbikes.weather_current as wc, dublinbikes.bike_weather_assoc as bw WHERE bw.weather_station = wc.name AND bw.bike_station_id = {};".format(station)
        prediction_query = pd.read_sql(weather_data, conn)
        # update prediction table to include hour and day info
        prediction_query = prediction_query.assign(d1=int(day_bin[-1]),d2=int(day_bin[-2]),d3=int(day_bin[-3]),h1=int(hour_bin[-1]),h2=int(hour_bin[-2]),h3=int(hour_bin[-3]),h4=int(hour_bin[-4]),h5=int(hour_bin[-5]))
        # make the predictions
        predicted_bikes_noCov = noCovModel.predict(prediction_query)
        predicted_bikes_cov = covModel.predict(prediction_query)
        # update the table with the predictions
        noCov_insert = "INSERT INTO dublinbikes.station_day_prediction (number,day,covid,pred_h_{}) VALUES ({}, {}, {}, {});".format(hour,station,day,0,predicted_bikes_noCov[0])
        noCov_update = "UPDATE dublinbikes.station_week_prediction SET pred_h_{} = {} WHERE (number = {},day = {},covid = {});".format(hour,predicted_bikes_noCov[0],station,day,0)
        cov_insert = "INSERT INTO dublinbikes.station_day_prediction (number,day,covid,pred_h_{}) VALUES ({}, {}, {}, {});".format(hour,station,day,1,predicted_bikes_cov[0])
        cov_update = "UPDATE dublinbikes.station_week_prediction SET pred_h_{} = {} WHERE (number = {},day = {},covid = {});".format(hour,predicted_bikes_cov[0],station,day,1)
        try:
            conn.execute(noCov_insert)
        except:
            conn.execute(noCov_update)
        try:
            conn.execute(cov_insert)
        except:
            conn.execute(cov_update)
    
    
def main():
    with engine.connect() as conn:
        station = "SELECT number FROM dublinbikes.static_data"
        stat_df = pd.read_sql(station,conn)
    for station in stat_df.number:
         bikesPredict(station)

if __name__ == '__main__':
    main()
