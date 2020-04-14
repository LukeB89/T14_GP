'''
Created on 16 Feb 2020

@author: Ruth Holmes
'''

from flask import Flask, render_template, g, jsonify, request
from sqlalchemy import create_engine
from configparser import ConfigParser

# read DataBase info from the config file
config = ConfigParser()
config.read("config.ini")
options = config["DataBase"]

app = Flask(__name__, static_url_path='/static')

engine = create_engine("mysql://" + options["user"] + ":" + options["passwd"] + "@"
                       + options["host"] + "/" + options["database"])
engine.connect()

bulk_data = """
        select s.number, s.address, b.status, b.available_bike_stands, b.available_bikes, 
            w.weather_main, w.weather_icon, w.main_temp, w.main_feels_like, w.rain_1h,
            s.banking, s.bonus, s.lat, s.lng
        from static_data s, bikes_current b, weather_current w, bike_weather_assoc a
        where s.number = b.number and b.number = a.bike_station_id and a.weather_station = w.name
        """
station_data = "select s.number, s.address from static_data s"
ordered = " order by s.address asc"


@app.route("/index")
@app.route("/")
def index_page():
    # request co-ordinates, name, number & dynamic bikes/weather data from DataBase for each bike station
    statinfo = engine.execute(bulk_data+ordered)
    return render_template('index.html', title='Map', statinfo=statinfo)


@app.route("/index/route")
def index_page_route():
    statinfo = engine.execute(bulk_data+ordered)
    coords = {"dest":[float(request.args.get('tolat')),float(request.args.get('tolong'))],
            "origin":[float(request.args.get('fromlat')), float(request.args.get('fromlong'))]}
    return render_template('routeindex.html', title='Map-Route', statinfo=statinfo, coordinates=coords)


@app.route("/info")
def info_page():
    stat_addr = engine.execute(station_data+ordered)
    return render_template('info.html', title='Station Information',stat_addr = stat_addr, statinfo="none")  


@app.route("/info/<stat_id>")
def info_page_refined(stat_id):
    statinfo = engine.execute(bulk_data+" and s.number = " + stat_id+ordered)
    stat_addr = engine.execute(station_data+ordered)
    return render_template('info.html',title='Station Information', stat_addr = stat_addr,  statinfo = statinfo, page=stat_id)  

@app.route("/get_weather_dublin")
def get_weather_dublin():
    """Allows client side to get up-to-date weather Info for dublin"""
    dublin_weather = engine.execute("""
        select w.main_temp, w.main_feels_like, w.weather_main, w.weather_icon, w.weather_description
        from weather_current w
        where w.name = "Dublin"
        """)

    for row in dublin_weather:
        response = jsonify(dict(row))
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


@app.route("/get_station_current")
def get_station_current():
    """Allows client side to request current dynamic data associate with a given bike station ID"""
    station_id = request.args.get("id")
    station_weather = engine.execute(bulk_data + "and s.number = " + station_id)
    for row in station_weather:
        response = jsonify(dict(row))
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


@app.route("/date")
def get_station_date():
    """Allows client side to request current based on day and station selected"""
    station_id = request.args.get("id")
    sql = """
        SELECT min(wf.dt) as dt, wf.day 
        FROM dublinbikes.bike_weather_assoc bw, dublinbikes.weather_forecast wf 
        WHERE wf.name = bw.weather_station AND bike_station_id = {} GROUP BY wf.day;""".format(station_id)
    current_date = engine.execute(sql)
    response = {
            "days": {}
        }
    for row in current_date:
        day = row[1]
        dt = row[0]
        response["days"][day] = dt

    return response


@app.route("/get_weather_forecast")
def get_weather_forecast():
    """Allows client side to request weather forecast data associated with a given bike station ID"""
    station_id = request.args.get("id")
    day_num = request.args.get("day")

    sql = """
        select f.icon
        from weather_forecast f, bike_weather_assoc a
        where a.bike_station_id = %s and a.weather_station = f.name and f.day = %s
        """ % (station_id, day_num)

    forecast = engine.execute(sql)
    response = []
    for row in forecast:
        response.append(dict(row)["icon"])

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/get_station_prediction")
def get_station_prediction():
    """Defines behavior when clients request station/bike usage predictive data for a given station id"""

    # response json format
    # chart names should correspond to the container element ids'used in info.html
    """
        stationIdData:{[
            bikesByHour: {
                dataSets: {
                    Monday: [seriesData], 
                    Tuesday: [seriesData],
                    ...
                },
                xAxisLabels: ["05:00", "07:00", "09:00"... ]
                seriesLabels: ["Free Bikes", "Free Stands"]
            },
            bikesByWeekday: {
                dataSets: {
                    week: [seriesData]
                },
                xAxisLabels: ["Sunday", "Monday", "Tuesday"... ]
                seriesLabels: ["Station Usage"]
            }
        ]}
    """

    def convert_hours(hour):
        """ utility function, converts an hour of the day entered in the string format 'pred_h_05' (as
        recorded in the RDS database) into the 24 hour clock representation '05:00' """

        # split the string into a list using underscores as the delimiter & select the last index in the list
        n = hour.split("_")[-1]

        # if n is only a single character; add a 0 to the front of n
        if len(n) == 1:
            n = "0" + n

        return n + ":00"

    station_id = request.args.get("id")
    # get the daily trend from the database

    prediction_by_day = engine.execute("""
                select *
                from  station_week_prediction p
                where p.number = %s
                """ % station_id)

    # get the hourly trend from the database
    prediction_by_hour = engine.execute("""
                    select *
                    from  station_day_prediction p
                    where p.number = %s
                    """ % station_id)

    # get the total number of bike stands for this station
    stands = engine.execute("""
                    select bike_stands
                    from  bikes_current c
                    where c.number = %s
                    """ % station_id)

    # build the framework of the response json
    response = {
        "bikesByWeekday": {
            "dataSets": {
                "week": {}
            },
            "xAxisLabels": [],
            "seriesLabels": []
        },
        "bikesByHour": {
            "dataSets": {},
            "xAxisLabels": [],
            "seriesLabels": []
        },
        "bikesByHourCovid": {
            "dataSets": {},
            "xAxisLabels": [],
            "seriesLabels": []
        }
    }

    # populate the response json
    for row in stands:
        stands = dict(row)
    print(stands["bike_stands"])

    for row in prediction_by_day:
        temp = dict(row)
        temp.pop("number")
        response["bikesByWeekday"]["dataSets"]["week"] = [temp]
        response["bikesByWeekday"]["seriesLabels"].append("Station Usage")
    response["bikesByWeekday"]["xAxisLabels"] = ["sun", "mon", "tue", "wed", "thur", "fri", "sat"]

    for row in prediction_by_hour:
        temp = dict(row)
        temp.pop("number")
        day = temp.pop("day")
        covid = temp.pop("covid")

        # convert the names of the remaining keys/datafields into the 24-hour format
        someDict = {}
        for key in temp:
            someDict[convert_hours(key)] = temp[key]
        temp = someDict

        # rectify values where the predicted number of bikes is negative
        for i in temp:
            if temp[i] < 0:
                temp[i] = 0

        if covid:
            response["bikesByHourCovid"]["dataSets"][day] = ["bikes", "stands"]
            response["bikesByHourCovid"]["dataSets"][day][0] = temp
            response["bikesByHourCovid"]["xAxisLabels"] = list(temp.keys())

        else:
            response["bikesByHour"]["dataSets"][day] = ["bikes", "stands"]
            response["bikesByHour"]["dataSets"][day][0] = temp
            response["bikesByHour"]["xAxisLabels"] = list(temp.keys())

    response["bikesByHour"]["seriesLabels"] = ["Free Bikes", "Free Stands"]
    response["bikesByHourCovid"]["seriesLabels"] = ["Free Bikes", "Free Stands"]

    # generate data representing the number of free bike stands from
    # the number of free bikes & the total number of stands
    for data in ["bikesByHour", "bikesByHourCovid"]:
        for day in response[data]["dataSets"]:
            series = response[data]["dataSets"][day]

            series[1] = {}
            for key in list(series[0].keys()):
                series[1][key] = abs(series[0][key] - stands["bike_stands"])

    # convert response into json
    response = jsonify(response)
    # add CORs security header to response : required for compatibility
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# allows us to run directly with python i.e. don't have to set env variables each time
if __name__ == '__main__':
    app.run(debug=True)
