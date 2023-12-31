from flask import Flask, render_template,request, json, url_for, Blueprint
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import flash
# from .models import GPDetails, UserDetails, PuffHistory
# from .models import *
from . import *

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
def home():
    return(render_template("Home.html"))

@bp.route("/")
def initial():
    return(render_template("Initial_Page.html"))

# @bp.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
# def add_user():
#     return(render_template("Login_page_template.html"))

@bp.route("/map")
def aqiview():
    return render_template('Air_Quality_Map.html')

@bp.route("/signup")
def signupview():
    return render_template('Sign_up_page_template.html')

### Test on the form submission and visualisation in template ###
@bp.route("/login")
def loginview():
    return render_template('Login_page_template.html')

@bp.route("/logbook", methods=['GET', 'POST'])
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
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # shows the hashed password in decoded format
            # data = UserDetails(first_name, last_name, email, password, 'NULL', 'NULL', 'NULL', 3)
            # db.session.add(data)
            # db.session.commit()
            return render_template("New_Logbook_template.html",
                                first_name = first_name,
                                last_name = last_name,
                                email = email,
                                password = hashed_password)
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


@bp.route("/update", methods = ['GET', 'POST'])
def updateview():
    return render_template('Update_Details.html')

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

app = create_app()
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')