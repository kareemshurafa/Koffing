from flask import Flask, render_template,request, json, url_for
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Add database
#heroku config --app koffing
#The name NEEDS to start with postgresql, not postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'

#Initialize database
db = SQLAlchemy(app)

class UserData(db.Model):
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique=True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    # def __init__(self, user, age, medication, dose):
    #     self.user = user
    #     self.age = age
    #     self.medication = medication
    #     self.dose = dose
    
    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
def add_user():
    return(render_template("sql-data.html"))


@app.route("/")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@app.route("/map")
def mapview():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')