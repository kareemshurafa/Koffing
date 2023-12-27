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

class AsthmaInfo(db.Model):
    #Create a foreignkey to link to users, refer to primary key of the user
    id = db.Column(db.Integer, primary_key=True)
    #Following info is nullable as may not want to put in this info
    step = db.Column(db.String(10), nullable = True) #For what step of asthma you're in? Check
    scores = db.Column(db.Integer, nullable = True) #For ACT scores
    variability = db.Column(db.Integer, nullable = True)# For peak flow variability
    fev1 = db.Column(db.Integer, nullable = True) 
    fev1fevcratio = db.Column(db.Integer, nullable=True)
    gpname = db.Column(db.String(100), nullable = True)
    gpsurname = db.Column(db.String(100), nullable = True)
    gpcode = db.Column(db.Integer, nullable = True)
    gptele = db.Column(db.Integer, nullable = True)
    gpaddy = db.Column(db.String(500), nullable=True)

    # info_id = db.Column(db.Integer, db.ForeignKey(userdata.id))   

class AsthmaLog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # log_id = db.Column(db.Integer, db.ForeignKey(userdata.id))
    medtype = db.Column(db.String(100), nullable = False)
    dosageamt = db.Column(db.Integer, nullable = False)
    puffno = db.Column(db.Integer, nullable = False)
    puffdate = db.Column(db.DateTime, default=datetime.utcnow)
    pufftime = db.Column(db.DateTime, default=datetime.utcnow) #Need to double check if this actually outputs the time
    
class UserData(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique=True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    password = db.Column(db.String(20),nullable=False)
    addy = db.Column(db.String(500), nullable = True)
    DOB = db.Column(db.DateTime, default=datetime.utcnow)
    
    #User can have many logs
    logs = db.relationship('AsthmaLog', backref ='log')
    #To call info from the user data, you would do log.name, log.email, etc

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
    return render_template('Air_Quality_Map.html')

@app.route("/signup")
def signupview():
    return render_template('Sign_up_page_template.html')

@app.route("/login")
def loginview():
    return render_template('Login_page_template.html')

@app.route("/logbook")
def logbookview():
    return render_template('Logbook_template.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0')