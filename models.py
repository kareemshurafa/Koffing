import .extensions
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .app import app

db=SQLAlchemy()

class UserDetails(db.Model):
    __tablename__ = 'UserDetails'
    id = db.Column(db.Integer,primary_key = True)
    #Login Details
    firstname = db.Column(db.String(30),nullable = False)
    surname = db.Column(db.String(30),nullable = False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    password = db.Column(db.String(128),nullable = False)

    phonenum = db.Column(db.Integer,nullable=True,unique=True)
    dob = db.Column(db.DateTime,default=datetime.utcnow,nullable=True)
    address = db.Column(db.String(50),nullable=True)

    GPname = db.Column(db.String(200),nullable=True)
    GPsurname = db.Column(db.String(50),nullable=True)
    GPcode = db.Column(db.String(30),nullable=True)
    GPaddress = db.Column(db.String(200), nullable = True)
    GPnum = db.Column(db.Integer(),nullable=True) 

    #Creating a one-to-many relationship to puffhistory
        #backref - gives email when puff.email is called
        #lazy = True - load the data as necessary 
    asthmapuffs = db.relationship('PuffHistory',backref='id',lazy=True)
    asthmadetails = db.relationship('AsthmaDetails',backref='id',lazy=True)

class AsthmaDetails(db.Model):
    __tablename__ = 'AsthmaDetails'
    id = db.Column(db.Integer,primary_key = True)
    asthmastep = db.Column(db.String(50),nullable=True)
    actscore = db.Column(db.String(50),nullable=True)
    peakflowvar =  db.Column(db.String(50),nullable=True)
    fev1 = db.Column(db.String(50),nullable=True)
    fevsratio = db.Column(db.String(50),nullable=True)
    peakflowreading = db.Column(db.String(50),nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('UserDetails.id'))

class PuffHistory(db.Model):
    __tablename__='PuffHistory'
    id = db.Column(db.Integer,primary_key = True)
    inhalertype = db.Column(db.String(40),nullable=False)
    medname = db.Column(db.String(40),nullable=False)
    dosageamt = db.Column(db.Integer,nullable=False)
    puffno = db.Column(db.Integer,nullable=False)
    datetaken = db.Column(db.DateTime,default=datetime.utcnow)
    timetaken = db.Column(db.DateTime,default=datetime.utcnow) #NEED TO MAKE SURE JUST TIME

    user_id = db.Column(db.Integer, db.ForeignKey('userdetails.id'))

with app.app_context():
    db.init_app(app)
    db.create_all()