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

class TestModel(db.Model):
    __tablename__ = 'testmodel'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    inhaler = db.Column(db.String(200),nullable = False)

    def __init__(self,name,inhaler):
        self.name = name
        self.inhaler = inhaler 
    
    def __repr__(self):
        return '<User %r>' % self.id

# class UserData(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(200), nullable = False)
#     email = db.Column(db.String(120), nullable = False, unique=True)
#     date_added = db.Column(db.DateTime, default = datetime.utcnow)
#     password = db.Column(db.String(20),nullable=True)
#     addy = db.Column(db.String(500), nullable = True)
#     DOB = db.Column(db.DateTime, default=datetime.utcnow)
    
#     #User can have many logs
#     #logs = db.relationship('AsthmaLog', backref ='log')
#     #To call info from the user data, you would do log.name, log.email, etc

#     def __init__(self, name, email, date_added, password, addy, DOB):
#         self.name = name
#         self.email = email
#         self.date_added = date_added
#         self.password = password 
#         self.addy = addy  
#         self.DOB = DOB
    
#     def __repr__(self):
#         return '<User %r>' % self.id

# with app.app_context():
#     db.create_all()

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