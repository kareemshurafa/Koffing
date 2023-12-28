from flask import Flask, render_template,request, json, url_for
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import flash

ENV = "dev"

app = Flask(__name__)

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

app.config['SECRET_KEY'] = 'Koffing123!' #Should likely hide this

db = SQLAlchemy(app)

#Initialize database

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

with app.app_context():
    db.create_all()

@app.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
def add_user():
    return(render_template("html/Login_page.html"))

@app.route("/")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@app.route("/map")
def aqiview():
    return render_template('map.html')

@app.route("/aqi")
def mapview():
    return render_template('aqi_widget.html')

@app.route("/history")
def historyview():
    return render_template('historical_data.html')

@app.route("/signup")
def signupview():
    return render_template('Sign_up_page_template.html')

### Test on the form submission and visualisation in template ###

# @app.route("/submitted", methods=['GET', 'POST'])
# def submittedview():
#     if request.method == 'POST':
#         first_name = request.form.get('First_name')
#         last_name = request.form.get('Last_name')
#         email = request.form.get('Email_Address')
#         password = request.form.get('Password')
#     return render_template("submitted.html",
#                            first_name = first_name,
#                            last_name = last_name,
#                            email = email,
#                            password = password)


@app.route("/login")
def loginview():
    return render_template('Login_page_template.html')

@app.route("/logbook", methods=['GET', 'POST'])
def logbookview():
    # This differentiates between the POST requests from signing up and updating the extra details form
    # What we need to do is be clear on how to handle first signing up and then normal logging in in terms of what is shown in the logbook
    # That might have to do with Flask User Sessions but we'll see - main thing is to get the connection with the database !!
    if request.method == 'POST':
        if "sign_up_form" in request.form:
            first_name = request.form.get('First_name')
            last_name = request.form.get('Last_name')
            email = request.form.get('Email_Address')
            password = request.form.get('Password')
            return render_template("New_Logbook_template.html",
                                first_name = first_name,
                                last_name = last_name,
                                email = email,
                                password = password)
        elif "update_details_form" in request.form:
            phone_number = request.form.get('phone_number')
            dob = request.form.get('dob')
            address = request.form.get('address')
            gp_name = request.form.get('gp_name')
            gp_surname = request.form.get('gp_surname')
            gp_code = request.form.get('gp_code')
            gp_phone_number = request.form.get('gp_phone_number')
            gp_address = request.form.get('gp_address')
            return render_template("New_Logbook_template.html",
                                   phone_number = phone_number,
                                   dob = dob,
                                   address = address,
                                   gp_name = gp_name,
                                   gp_surname = gp_surname,
                                   gp_code = gp_code,
                                   gp_phone_number = gp_phone_number,
                                   gp_address = gp_address)


@app.route("/update", methods = ['GET', 'POST'])
def updateview():
    return render_template('Update_Details.html')

#Create asthma log page:
@app.route('/testlog', methods = ['GET','POST'])
def testlog():
    form = AsthmaLogForm()
    med = None

    #Validate form
    if form.validate_on_submit(): 
        #if submitted, make name this then clear it
        med = form.med.data
        form.med.data = ''
    return render_template("testasthmalogform.html",
                           form = form,
                           med = med)


# @app.route('/user/add', methods = ['GET','POST'])
# def add_users():
#     name = None
#     form = UserForm()
        
#     #Validate form
#     if form.validate_on_submit(): 
#         name = form.name.data
#         user = UserData.query.filter_by(name = form.name.data).first()
#         form.name.data = '' 
#         flash("User Made Successfully")
    
#     return render_template("add_user.html",
#                            form = form)

@app.route('/test')
def index():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        inhaler = request.form['inhaler']
        # print(name,inhaler)
        if name =='' or inhaler=='':
            return render_template('test.html', message='Please enter required fields')

        if db.session.query(TestModel).filter(TestModel.name == name).count() == 0:
             #Says that the customer does not exist
            data = TestModel(name,inhaler) #Form data that we want to submit
            db.session.add(data)
            db.session.commit()
            return "<h2 style='color:red'>Yipee!</h2>"
        return render_template('test.html', message='You have already submitted')

#Create a form class
class AsthmaLogForm(FlaskForm):
    med = StringField("What puff did you take?", validators = [DataRequired()]) #If not filled out, makes sure it gets filled
    submit = SubmitField("Puff!")

class UserForm(FlaskForm):
    name = StringField("What name?", validators = [DataRequired()]) #If not filled out, makes sure it gets filled   
    email = StringField("Email", validators = [DataRequired()]) #Can change to email validator
    submit = SubmitField("Submitf!")

if __name__ == "__main__":
    app.run(host='0.0.0.0')