"""
Created on 06 Mar 2020
Version: 0.1.01
@author: Luke Byrne

Methods for predicting and updating hourly prediction tables in the database
"""
# Set up libraries
import pandas as pd
import pickle
from sqlalchemy import create_engine
from configparser import ConfigParser


# Configure the connection
config = ConfigParser()
config.read("config.ini")
options = config["DataBase"]
engine = create_engine("mysql://" + options["user"] + ":" + options["passwd"] + "@" + options["host"] + "/" + options["database"])
hour_assoc = [0,0,3,3,3,6,6,6,9,9,9,12,12,12,15,15,15,18,18,18,21,21,21,0]
def bikesPredict(station,day,hour):
    # configure day and hour
    forecast_hour = hour_assoc[hour]
    hour_bin = '{0:05b}'.format(hour)
    day_bin = '{0:03b}'.format(day)
    # import the model to be used
    with open('models/dBikePredictNoCov_station_{}.pkl'.format(station), 'rb') as handle:
        noCovModel = pickle.load(handle)
    with open('models/dBikePredictCovData_station_{}.pkl'.format(station), 'rb') as handle:
        covModel = pickle.load(handle)
    with engine.connect() as conn:
        weather_data = "SELECT wf.id, wf.main_temp, wf.main_humidity, wf.wind_speed FROM dublinbikes.weather_forecast as wf, dublinbikes.bike_weather_assoc as bw WHERE bw.weather_station = wf.name AND bw.bike_station_id = {} AND wf.day = {} AND wf.hour = {};".format(station,day,forecast_hour)
        prediction_query = pd.read_sql(weather_data, conn)
        # update prediction table to include hour and day info
        prediction_query = prediction_query.assign(d1=0,d2=0,d3=0,h1=0,h2=0,h3=0,h4=0,h5=0)
        # make the predictions
        prediction_query.at[0,'d1'] = int(day_bin[-1])
        prediction_query.at[0,'d2'] = int(day_bin[-2])
        prediction_query.at[0,'d3'] = int(day_bin[-3])
        prediction_query.at[0,'h1'] = int(hour_bin[-1])
        prediction_query.at[0,'h2'] = int(hour_bin[-2])
        prediction_query.at[0,'h3'] = int(hour_bin[-3])
        prediction_query.at[0,'h4'] = int(hour_bin[-4])
        prediction_query.at[0,'h5'] = int(hour_bin[-5])
        predicted_bikes_noCov = noCovModel.predict(prediction_query)
        predicted_bikes_cov = covModel.predict(prediction_query)
        # update the table with the predictions
        noCov_insert = "INSERT INTO dublinbikes.station_day_prediction (number,day,covid,pred_h_{}) VALUES ({}, {}, {}, {});".format(hour,station,day,0,predicted_bikes_noCov[0])
        noCov_update = "UPDATE dublinbikes.station_day_prediction SET pred_h_{} = {} WHERE (number = {}) AND (day = {}) AND (covid = {});".format(hour,predicted_bikes_noCov[0],station,day,0)
        cov_insert = "INSERT INTO dublinbikes.station_day_prediction (number,day,covid,pred_h_{}) VALUES ({}, {}, {}, {});".format(hour,station,day,1,predicted_bikes_cov[0])
        cov_update = "UPDATE dublinbikes.station_day_prediction SET pred_h_{} = {} WHERE (number = {}) AND (day = {}) AND (covid = {});".format(hour,predicted_bikes_cov[0],station,day,1)
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
         for day in range(7):
             for hour in range(24):
                 bikesPredict(station, day, hour)

if __name__ == '__main__':
    main()
