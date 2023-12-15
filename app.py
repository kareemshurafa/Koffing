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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Koffing123!' #Should likely hide this

@app.route('/database/test', methods = ['GET', 'POST'] ) #Double check these methods
def add_user():
    return(render_template("html/Login_page.html"))

@app.route("/")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

@app.route("/map")
def mapview():
    return render_template('map.html')

@app.route("/signup")
def signupview():
    return render_template('Sign_up_page_template.html')

@app.route("/login")
def loginview():
    return render_template('Login_page_template.html')

@app.route("/logbook")
def logbookview():
    return render_template('Logbook_template.html')

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
    
@app.route('/user/add', methods = ['GET','POST'])
def add_user():
    return render_template("add_user.html",
                           form = form,
                           med = med)

#Create a form class
class AsthmaLogForm(FlaskForm):
    med = StringField("What puff did you take?", validators = [DataRequired()]) #If not filled out, makes sure it gets filled
    submit = SubmitField("Puff!")

def UserForm(FlaskForm):
    name = StringField("What name?", validators = [DataRequired()]) #If not filled out, makes sure it gets filled   
    name = StringField("Email", validators = [DataRequired()]) #Can change to email validator
    submit = SubmitField("Submitf!")

if __name__ == "__main__":
    app.run(host='0.0.0.0')