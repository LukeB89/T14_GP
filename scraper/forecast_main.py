'''
Created on 10 Feb 2020
Version: 0.1
@author: Luke Byrne
main method to call scrapers
'''
# Import liberies for use of the  
import get_bikes_data as bikes
import get_weather_data as weather
import csv

def main():
    
#   main code which is tasked with running the JSON Parser
#   keeps a log to ensure the returned API information doesnt crash the program.
    
    with open('log.txt', 'a', newline='') as file:
        weather.get_forecast_all()
    return
if __name__ == '__main__':
    main()
