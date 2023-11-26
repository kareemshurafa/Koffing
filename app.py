from flask import Flask, render_template,request, json, url_for
import requests
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True #Local database
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'
else:
    app.debug = False #Production database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class UserData(db.Model):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), unique=True) #Sets the string to be max 200, and sets every customer to be unique
    age = db.Column(db.Integer)
    medication = db.Column(db.String(40))
    dose = db.Column(db.Integer)

    def __init__(self, user, age, medication, dose):
        self.user = user
        self.age = age
        self.medication = medication
        self.dose = dose
    
    def __repr__(self):
        return '<User %r>' % self.user

with app.app_context():
    db.create_all()

    db.session.delete()
    db.session.add(UserData('admin', 20, "bleh", 4))
    db.session.commit()


    users = UserData.query.all()


@app.route("/home")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@app.route("/map")
def mapview():
    return render_template('map.html')

@app.route("/database")
def databaseview():
    return users


if __name__ == "__main__":
    app.run(host='0.0.0.0')