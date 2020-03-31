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
def index_page():
    # request co-ordinates, name, number & dynamic bikes/weather data from DataBase for each bike station
    statinfo = engine.execute(bulk_data+ordered)
    return render_template('index.html', title='Map', statinfo=statinfo)


@app.route("/index/route")
def index_page_route():
    statinfo = engine.execute(bulk_data+ordered)
    coords = {"dest":[float(request.args.get('tolat')),float(request.args.get('tolong'))],
            "origin":[float(request.args.get('fromlat')), float(request.args.get('fromlong'))]}
    return render_template('routeindex.html', title='Map', statinfo=statinfo, coordinates=coords)


@app.route("/info")
def info_page():
    stat_addr = engine.execute(station_data+ordered)
    return render_template('info.html', stat_addr = stat_addr, stat_info="none")  # pulls home.html template from templates folder


@app.route("/info/<stat_id>")
def info_page_refined(stat_id):
    statinfo = engine.execute(bulk_data+" and s.number = " + stat_id+ordered)
    stat_addr = engine.execute(station_data+ordered)
    return render_template('info.html', stat_addr = stat_addr,  statinfo = statinfo)  # pulls home.html template from templates folder


@app.route("/")
def bikemap():
    statinfo = engine.execute('select number, address, lat, lng from static_data')
    bikenos = engine.execute('select number, available_bikes from bikes_current')
    return render_template('map.html', title='Map', statinfo=statinfo, bikenos=bikenos)


@app.route("/route")
def routemap():
    statinfo = engine.execute('select number, address, lat, lng from static_data')
    return render_template('route.html', title='Route', statinfo=statinfo)


@app.route("/get_weather_dublin")
def get_weather_dublin():
    """Allows client side to get up-to-date weather Info for dublin"""
    dublin_weather = engine.execute("""
        select w.main_temp, w.main_feels_like, w.weather_main, w.weather_icon
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


# allows us to run directly with python i.e. don't have to set env variables each time
if __name__ == '__main__':
    app.run(debug=True)
