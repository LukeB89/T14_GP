'''
Created on 16 Feb 2020

@author: Ruth Holmes
'''

from flask import Flask, render_template, g, jsonify
from sqlalchemy import create_engine
from configparser import ConfigParser

# read DataBase info from the config file
config = ConfigParser()
config.read("config.ini")
options = config["DataBase"]

app = Flask(__name__)

engine = create_engine("mysql://" + options["user"] + ":" + options["passwd"] + "@"
                       + options["host"] + "/" + options["database"])
engine.connect()
 
# @app.route("/test")
# def dub_bikes():
#     l1 = engine.execute('select name from static_data')  #
#     return render_template('home.html', l1=l1)  # pulls home.html template from templates folder
#  
@app.route("/index")
def index_page():
    statinfo = engine.execute('select number, address, lat, lng from static_data')
    return render_template('index.html', title='Map', statinfo=statinfo)
  
@app.route("/info")
def info_page():
    stat_addr = engine.execute('select number, address from static_data')
    return render_template('info.html', stat_addr = stat_addr, stat_info="none")  # pulls home.html template from templates folder

@app.route("/info/<stat_id>")
def info_page_refined(stat_id):
    stat_info = engine.execute('select * from static_data where number = {}'.format(stat_id))
    print(stat_info)
    stat_addr = engine.execute('select number, address from static_data')
    print(stat_addr)
    return render_template('info.html', stat_addr = stat_addr,  stat_info = stat_info)  # pulls home.html template from templates folder


@app.route("/")
def bikemap():
    statinfo = engine.execute('select number, address, lat, lng from static_data')
    return render_template('map.html', title='Map', statinfo=statinfo)


# allows us to run directly with python i.e. don't have to set env variables each time
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
