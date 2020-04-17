'''
Created on 10 Feb 2020
Version: 0.1
@author: Luke Byrne
main method to call scrapers
'''
# Import liberies for use
import get_bikes_data as bikes
import get_weather_data as weather
import csv

def main():
    # obtaining all of the forcasted data with a log should there be an error
    with open('log.txt', 'a', newline='') as file:
        log_out = csv.writer(file)
        try:
            weather.get_forecast_all()
        except:
            log_out.writerow(["Error detected in Weather Data retrieval."])
    return
# initial code to be run
if __name__ == '__main__':
    main()
