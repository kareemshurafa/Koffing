from flask import Flask, render_template, request, json, url_for, Blueprint, session, redirect, url_for, flash
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from flask_bcrypt import Bcrypt
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager

db=SQLAlchemy()
login_manager = LoginManager()

#--------------Models---------------------
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

    latitude = db.Column(db.Float(), nullable = True)
    longitude = db.Column(db.Float(), nullable = True)

    #Creating a one-to-many relationship to puffhistory
        #backref - gives email when puff.email is called
        #lazy = True - load the data as necessary 
    asthmapuffs = db.relationship('PuffHistory',backref='UserDetails',lazy=True)

# class AsthmaDetails(db.Model):
#     __tablename__ = 'AsthmaDetails'
#     id = db.Column(db.Integer,primary_key = True)
#     asthmastep = db.Column(db.String(50),nullable=True)
#     actscore = db.Column(db.String(50),nullable=True)
#     peakflowvar =  db.Column(db.String(50),nullable=True)
#     fev1 = db.Column(db.String(50),nullable=True)
#     fevsratio = db.Column(db.String(50),nullable=True)
#     peakflowreading = db.Column(db.String(50),nullable=True)

#     user_id = db.Column(db.Integer, db.ForeignKey('UserDetails.id'))

class PuffHistory(db.Model):
    __tablename__='PuffHistory'
    id = db.Column(db.Integer,primary_key = True)
    inhalertype = db.Column(db.String(40),nullable=False)
    medname = db.Column(db.String(40),nullable=True)
    dosageamt = db.Column(db.Integer,nullable=False)
    puffno = db.Column(db.Integer,nullable=False)
    datetaken = db.Column(db.DateTime,default=datetime.now().date())
    timetaken = db.Column(db.DateTime,default=datetime.now().time()) #NEED TO MAKE SURE JUST TIME
    peakflow = db.Column(db.Float,nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('UserDetails.id'))

#----------------------------------------------------------

def create_app(database_URI = 'postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'):
    app = Flask(__name__)

    ENV="dev"

    if ENV  == "dev":
        app.config['ENV'] = 'development'
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = database_URI
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_URI

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app)
    # login_manager.init_app(app) 

    app.register_blueprint(bp)
    return app

bp = Blueprint("main", __name__)

@bp.route("/home")
def homeview():
    return(render_template("Home.html"))

@bp.route("/home", methods = ['POST'])
def homepost():
    if request.method == 'POST':
        date_format = '%Y/%m/%d'
        time_format = '%H:%M %p'
        date = datetime.strptime(request.form.get('Date_taken'),date_format)
        time = datetime.strptime(request.form.get('Time_taken'),time_format)
        inhalertype = request.form.get('Inhaler_type')
        dosageamt = request.form.get('Dosage')
        puffno = request.form.get('Number_of_puffs')
        medname = request.form.get('Medname')
        # peakflow = request.form.get('peakflow')
        puff = PuffHistory(inhalertype = inhalertype,
                        medname = medname,
                        dosageamt = dosageamt,
                        puffno = puffno,
                        datetaken = date,
                        timetaken = time,
                        UserDetails = session['id'])    
        db.session.add(puff)
        db.session.commit()  

@bp.route("/")
def initial():
    return(render_template("Initial_Page.html"))

# @bp.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
# def add_user():
#     return(render_template("Login_page_template.html"))

@bp.route("/mapinfo")
def aqiview():
    tester = db.session.query(UserDetails).filter_by(email=session['email']).first()
    tester.address = "W2 3ET"
    address = tester.address
    return render_template('Air_Quality_Map.html', address = address)

@bp.route("/airqualitystats")
def statsview():
    return render_template("Air_Quality_Stats.html")

@bp.route("/signup")
def signupview():
    return render_template("Sign_up_page_template.html")
    
@bp.route("/signup", methods=['POST'])
def signuppost():
    if request.method == 'POST':
        name = request.form.get('First_name')
        surname = request.form.get('Last_name')
        email = request.form.get('Email_Address')
        password = request.form.get('Password')
        confpass = request.form.get('Confirm_Password')
        # if password != confpass:
        #     # return redirect("/signup")
        #     flash("Passwords do not match!")
        # else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # shows the hashed password in decoded format
        data = UserDetails(firstname=name, surname=surname, email=email, password=hashed_password)
        db.session.add(data)
        db.session.commit()
    return redirect("/login")

### Test on the form submission and visualisation in template ###
@bp.route("/login")
def loginview():
#After logging in, have to m
    return render_template('Login_page_template.html')

@bp.route("/asthmainfo")
def asthmainfoview():
    return render_template('Asthma_Info.html')

@bp.route("/faq")
def faqview():
    return render_template("FAQPage.html")

### Creating a login_post route to handle login logic and re-routing ###
@bp.route("/login", methods=['POST'])
def loginpost():
    Email = request.form.get('Email')
    password = request.form.get('Password')
 
    # Boolean check if they have an account in the database
    exists = db.session.query(UserDetails).filter_by(email=Email).first() is not None

    # If they do not have an account - redirect to sign-up
    if not exists:
        return redirect("/signup")
    
    # Obtain record
    record = db.session.query(UserDetails).filter_by(email=Email).first()
    
    # Boolean check if password is correct
    pswrd = bcrypt.check_password_hash(record.password, password)

    # If they use an incorrect password - redirect to try again
    if not pswrd:
        return redirect("/login")

    # All checks passed - create user session and redirect to home page
    session['logged_in'] = True
    session['id'] = record.id
    session['email'] = Email
    return redirect("/home")

@bp.route("/logbook", methods=['GET', 'POST'])
def logbookview():
    if not session.get('logged_in'):
        return "you are not logged in - please login before accesing the logbook"

    # This differentiates between the POST requests from signing up and updating the extra details form
    # What we need to do is be clear on how to handle first signing up and then normal logging in in terms of what is shown in the logbook
    # That might have to do with Flask User Sessions but we'll see - main thing is to get the connection with the database !!
    
    tester = db.session.query(UserDetails).filter_by(email=session['email']).first()
    # tester = db.session.query(UserDetails).filter_by(email="test@gmail.com").first()
    # tester.address = "Wellington House, 133-135 Waterloo Road, London, SE1 8UG"
    # db.commit()
    name = tester.firstname
    surname = tester.surname
    email = tester.email

    phonenum = tester.phonenum
    dob = tester.dob
    address = tester.address

    GPname = tester.GPname
    GPsurname=tester.GPsurname
    GPcode = tester.GPcode
    GPaddress = tester.GPaddress
    GPnum = tester.GPnum

    #Just need to implement logic that checks consecutive submissions for each day
    # asthmastreak

    #Need to implement peak flow graph

    return render_template("New_Logbook_template.html",
                    first_name = name,
                    surname = surname,
                    email = email, 
                    phonenum = phonenum,
                    dob = dob,
                    address = address,
                    GPname = GPname,
                    GPsurname = GPsurname,
                    GPcode = GPcode,
                    GPnum = GPnum,)


    # if request.method == 'POST':
    #     if "sign_up_form" in request.form:  
    #         print(request.form)
    #         first_name = request.form.get('First_name')
    #         last_name = request.form.get('Last_name')
    #         email = request.form.get('Email_Address')
    #         password = request.form.get('Password')
    #         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # shows the hashed password in decoded format
            
    #         data = UserDetails(firstname=first_name, surname=last_name, email=email, password=hashed_password)
    #         #Need to implement checker if email has already been written
    #         db.session.add(data)
    #         db.session.commit()
    #         #Have to flash message that you have signed in
    #         return render_template("New_Logbook_template.html",
    #                             first_name = first_name,
    #                             last_name = last_name,
    #                             email = email, #
    #                             password = hashed_password)

    #     elif "update_details_form" in request.form:
    #         phone_number = request.form.get('phone_number')
    #         dob = request.form.get('dob')
    #         address = request.form.get('address')
    #         gp_name = request.form.get('gp_name')
    #         gp_surname = request.form.get('gp_surname')
    #         gp_code = request.form.get('gp_code')
    #         gp_phone_number = request.form.get('gp_phone_number')
    #         gp_address = request.form.get('gp_address')

    #         #This is a roundabout method, realistically:
    #         #Pull from the user's database, then render everything based on that, not get it straight from the form
    #         return render_template("New_Logbook_template.html",
    #                                phone_number = phone_number,
    #                                dob = dob,
    #                                address = address,
    #                                gp_name = gp_name,
    #                                gp_surname = gp_surname,
    #                                gp_code = gp_code,
    #                                gp_phone_number = gp_phone_number,
    #                                gp_address = gp_address)

    # return(render_template("New_Logbook_template.html"))

@bp.route("/update", methods = ['GET', 'POST'])
def updateview():
    return render_template('Update_Details.html')

@bp.route('/test')
def index():
    return render_template('test.html')

# @bp.route('/logout')
# def logoutview():
#     session.pop('logged_in', None)
#     return redirect("/")

# @bp.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         name = request.form['name']
#         inhaler = request.form['inhaler']
#         # print(name,inhaler)
#         if name =='' or inhaler=='':
#             return render_template('test.html', message='Please enter required fields')

#         if db.session.query(TestModel).filter(TestModel.name == name).count() == 0:
#              #Says that the customer does not exist
#             data = TestModel(name,inhaler) #Form data that we want to submit
#             db.session.add(data)
#             db.session.commit()
#             return "<h2 style='color:red'>Yipee!</h2>"
#         return render_template('test.html', message='You have already submitted')

app = create_app()
db.init_app(app)
bcrypt = Bcrypt(app)
app.secret_key = b'8dh3w90fph#3r'
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0')