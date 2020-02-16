'''
Created on 16 Feb 2020

@author: Ruth Holmes
'''

from flask import Flask, render_template

app = Flask(__name__)

test_data = [
    {
        'location': 'Capel Street',
        'num_bikes': '12',
        'weather': 'not great my dude'
    },
    {
        'location': 'Parnell Street',
        'num_bikes': '3',
        'weather': 'not great here either bruh'
    }
]


@app.route("/")
@app.route("/home")
def dub_bikes():
    return render_template('home.html', posts=test_data)  # pulls home.html template from templates folder


@app.route("/about")
def about():
    return render_template('home.html', title='About')


# allows us to run directly with python i.e. don't have to set env variables each time
if __name__ == '__main__':
    app.run(debug=True)
