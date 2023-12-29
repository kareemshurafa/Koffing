from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class LoginDetails(db.Model):
    __tablename__ = 'LoginDetails'
    email = db.Column(db.String(50), unique=True,primary_key = True) #Need to implement a check if this exists or not
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


class GPDetails(db.Model):
    __tablename__ = 'GPDetails'
    id = db.Column(db.Integer,primary_key = True)
    GPname = db.Column(db.String(200),nullable=False)
    GPcode = db.Column(db.String(30),nullable=False)
    address = db.Column(db.String(200), nullable = False)
    GPnum = db.Column(db.Integer(),nullable=True) #Set to unique=True?

    def __init__(self,GPname,GPcode,address,GPnum):
        self.GPname = GPname
        self.GPcode = GPcode
        self.address = address
        self.GPnum = GPnum

class UserDetails(db.Model):
    __tablename__ = 'UserDetails'
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(30),nullable = False)
    surname = db.Column(db.String(30),nullable = False)
    email = db.Column(db.String(50),nullable=False, unique=True)  
    phonenum = db.Column(db.Integer,nullable=True,unique=True)
    dob = db.Column(db.DateTime,default=datetime.utcnow)
    address = db.Column(db.String(50),nullable=True)
    #Creating a one-to-many relationship to puffhistory
        #backref - gives email when puff.email is called
        #lazy = True - load the data as necessary 
    asthmapuffs = db.relationship('PuffHistory',backref='email',lazy=True)
    
    #Linking GP to user - One to One relationship
    gpid = db.Column(db.Integer,db.ForeignKey(GPDetails.id))
    #Not 100% sure that this actually queries GPDetails.id

    def __init__(self,firstname,surname,email,phonenum,dob,address):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phonenum = phonenum
        self.dob = dob
        self.address = address


class PuffHistory(db.Model):
    __tablename__='PuffHistory'
    id = db.Column(db.Integer,primary_key = True)
    inhalertype = db.Column(db.String(40),nullable=False)
    medname = db.Column(db.String(40),nullable=False)
    dosageamt = db.Column(db.Integer,nullable=False)
    puffno = db.Column(db.Integer,nullable=False)
    datetaken = db.Column(db.DateTime,default=datetime.utcnow)
    timetaken = db.Column(db.DateTime,default=datetime.utcnow) #NEED TO MAKE SURE JUST TIME
    
    def __init__(self,inhalertype,medname,dosageamt,puffno,datetaken,timetaken):
        self.inhalertype = inhalertype
        self.medname = medname
        self.dosageamt=dosageamt
        self.puffno=puffno
        self.datetaken = datetaken
        self.timetaken = timetaken


# with app.app_context():
#     db.create_all()