from flask import Flask, render_template,request, json, url_for, Blueprint
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import flash
# from .models import GPDetails, UserDetails, PuffHistory
from .extensions import db

bp = Blueprint("bp", __name__)
# app = create_bp()

<<<<<<< HEAD
@bp.route("/")
def home():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@bp.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
def add_user():
    return(render_template("html/Login_page.html"))

@bp.route("/map")
def aqiview():
    return render_template('map.html')

@bp.route("/aqi")
def mapview():
    return render_template('aqi_widget.html')

@bp.route("/history")
def historyview():
    return render_template('historical_data.html')
=======
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
    return(render_template("Initial_Page.html"))

@app.route("/map")
def mapview():
    return render_template('Air_Quality_Map.html')
>>>>>>> main

@bp.route("/signup")
def signupview():
    return render_template('Sign_up_page_template.html')

### Test on the form submission and visualisation in template ###
@bp.route("/login")
def loginview():
    return render_template('Login_page_template.html')

@bp.route("/logbook", methods=['GET', 'POST'])
def logbookview():
    if request.method == 'POST':
        first_name = request.form.get('First_name')
        last_name = request.form.get('Last_name')
        email = request.form.get('Email_Address')
        password = request.form.get('Password')
    return render_template("Logbook_template.html",
                           first_name = first_name,
                           last_name = last_name,
                           email = email,
                           password = password)

#Create asthma log page:
@bp.route('/testlog', methods = ['GET','POST'])
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


@bp.route('/test')
def index():
    return render_template('test.html')

@bp.route('/submit', methods=['POST'])
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

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')