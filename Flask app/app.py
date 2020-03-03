'''
Created on 16 Feb 2020

@author: Ruth Holmes
'''

from flask import Flask, render_template, g, jsonify
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine("mysql://admin:SET14GP2020@dublinbikes.c69eptjjnovd.us-east-1.rds.amazonaws.com:3306/dublinbikes")
engine.connect()

@app.route("/test")
def dub_bikes():
    l1 = engine.execute('select name from static_data')  #
    return render_template('home.html', l1=l1)  # pulls home.html template from templates folder


@app.route("/")
def bikemap():
    return render_template('map.html', title='Map')


# allows us to run directly with python i.e. don't have to set env variables each time
if __name__ == '__main__':
    app.run(debug=True)
