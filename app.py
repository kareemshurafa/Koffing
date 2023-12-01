from flask import Flask, render_template,request, json, url_for
import requests
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@app.route("/map")
def mapview():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
