from flask import Flask, render_template, request, json, url_for, Blueprint, session, redirect, url_for, flash
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager
import yagmail

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

    phonenum = db.Column(db.String,nullable=True,unique=True)
    dob = db.Column(db.DateTime,default=datetime.utcnow,nullable=True)
    address = db.Column(db.String(50),nullable=True)

    GPname = db.Column(db.String(200),nullable=True)
    GPsurname = db.Column(db.String(50),nullable=True)
    GPcode = db.Column(db.String(30),nullable=True)
    GPaddress = db.Column(db.String(200), nullable = True)
    GPnum = db.Column(db.String(),nullable=True) 

    latitude = db.Column(db.Float(), nullable = True)
    longitude = db.Column(db.Float(), nullable = True)

    #Creating a one-to-many relationship to puffhistory
        #backref - gives email when puff.email is called
        #lazy = True - load the data as necessary 
    asthmapuffs = db.relationship('PuffHistory',backref='UserDetails',lazy=True)

class PuffHistory(db.Model):
    __tablename__='PuffHistory'
    id = db.Column(db.Integer,primary_key = True)
    inhalertype = db.Column(db.String(40),nullable=False)
    medname = db.Column(db.String(40),nullable=True)
    dosageamt = db.Column(db.Integer,nullable=False)
    puffno = db.Column(db.Integer,nullable=False)
    datetaken = db.Column(db.DateTime,default=datetime.now().date())
    timetaken = db.Column(db.DateTime,default=datetime.now().time())
    peakflow = db.Column(db.Float,nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('UserDetails.id'))

#--------------------App Creation---------------------

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

    app.register_blueprint(bp)
    return app

bp = Blueprint("main", __name__)

#------------------Routes---------------------

@bp.route("/")
def initial():
    try:
        if request.method == 'GET' and session['logged_in'] == True:
            return redirect("/home")
    except:
        return(render_template("Initial_Page.html"))
    
@bp.route("/signup", methods=['POST','GET'])
def signuppost():
    if request.method == 'POST':

        name = request.form.get('First_name')
        surname = request.form.get('Last_name')
        email = request.form.get('Email_Address')
        password = request.form.get('Password')
        confpass = request.form.get('Confirm_password')

        exists = db.session.query(UserDetails).filter_by(email=email).first() is not None

        if exists:
            error = "User already exists"
            return render_template('Sign_up_page_template.html', error = error)
        
        if password != confpass:
            error = "Passwords do not match"
            return render_template('Sign_up_page_template.html', error = error)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # shows the hashed password in decoded format
        data = UserDetails(firstname=name, surname=surname, email=email, password=hashed_password)
        
        
        db.session.add(data)
        db.session.commit()

        record = db.session.query(UserDetails).filter_by(email=email).first()

        session['logged_in'] = True
        session['id'] = record.id
        session['email'] = email
        return redirect("/home")
    try: 
        if request.method == 'GET' and session['logged_in'] == True:
            return redirect("/home")
    except:
        return render_template("Sign_up_page_template.html")
    
@bp.route("/login", methods=['POST', 'GET'])
def loginpost():
    
    error = None

    if request.method == 'POST':
        Email = request.form.get('Email')
        password = request.form.get('Password')
    
        # Boolean check if they have an account in the database
        exists = db.session.query(UserDetails).filter_by(email=Email).first() is not None

        # If they do not have an account - redirect to sign-up
        if not exists:
            error = "Invalid credentials"
            return render_template('Login_page_template.html', error = error)

        # Obtain record
        record = db.session.query(UserDetails).filter_by(email=Email).first()
        
        # Boolean check if password is correct
        pswrd = bcrypt.check_password_hash(record.password, password)

        # If they use an incorrect password - redirect to try again
        if not pswrd:
            error = "Invalid credentials"
            return render_template('Login_page_template.html', error = error)

        # All checks passed - create user session and redirect to home page
        session['logged_in'] = True
        session['id'] = record.id
        session['email'] = Email
        return redirect("/home")
    try:
        if request.method == 'GET' and session['logged_in'] == True:
            return redirect("/home")
    except:
        return render_template('Login_page_template.html')


@bp.route("/home", methods = ['POST','GET'])
def homepost():
    if not session.get('logged_in'):
        return render_template("Login_Redirect.html")
    
    puffs = db.session.query(PuffHistory).filter_by(user_id = session['id'])
    user = db.session.query(UserDetails).filter_by(id=session['id']).first()
    currAddress = user.address
    puffcount = puffs.count()

    if request.method == 'POST':
        if 'regpuff' in request.form:
            date_format = '%Y-%m-%d'
            time_format = '%H:%M'
            date = datetime.strptime(request.form.get('Date_taken'),date_format)
            time = datetime.strptime(request.form.get('Time_taken'),time_format)
            inhalertype = request.form.get('Inhaler_type')
            dosageamt = request.form.get('Dosage')
            puffno = request.form.get('Number_of_puffs')
            medname = request.form.get('Medname')

            #Defaults to current time if future time passed
            timediff = datetime.combine(datetime.today(), time.time()) - datetime.now()
            if timediff > timedelta(seconds=0):
                time = datetime.now()

            puff = PuffHistory(inhalertype = inhalertype,
                            medname = medname,
                            dosageamt = dosageamt,
                            puffno = puffno,
                            datetaken = date,
                            timetaken = time,
                            UserDetails = user)    
            db.session.add(puff)
            db.session.commit()  
            return redirect("/home")
        
        if 'quickpuff' in request.form:
            #Get current time and date, then submit the previous records details
            
            if puffs.count() != 0:
                user = db.session.query(UserDetails).filter_by(id=session['id']).first()
                lastpuff = db.session.query(PuffHistory).order_by(PuffHistory.id.desc()).filter_by(user_id = session['id']).first()
                date = datetime.now()
                time = datetime.now()
                inhalertype = lastpuff.inhalertype
                dosageamt = lastpuff.dosageamt
                puffno = lastpuff.puffno
                medname = lastpuff.medname

                puff = PuffHistory(inhalertype = inhalertype,
                                medname = medname,
                                dosageamt = dosageamt,
                                puffno = puffno,
                                datetaken = date,
                                timetaken = time,
                                UserDetails = user)    
                db.session.add(puff)
                db.session.commit()  
                return redirect("/home")
        if 'nopuffs' in request.form:
            return redirect("/home")
                
    if request.method == 'GET':
        return(render_template("Home.html",puffcount = puffcount, address = currAddress, api_key=os.environ.get('GOOGLE_API')))

@bp.route("/mapinfo")
def aqiview():
    if session.get('logged_in'):
        return render_template('Air_Quality_Map.html', api_key=os.environ.get('GOOGLE_API'))
    else:
        return render_template("Login_Redirect.html")
        

@bp.route("/airqualitystats")
def statsview():
    return render_template("Air_Quality_Stats.html")
    
@bp.route("/asthmainfo")
def asthmainfoview():
    if not session.get('logged_in'):
        return render_template("Login_Redirect.html")
    return render_template('Asthma_Info.html')

@bp.route("/faq")
def faqview():
    return render_template("FAQPage.html")

@bp.route("/logbook", methods=['GET', 'POST'])
def logbookview():
    if not session.get('logged_in'):
        return render_template("Login_Redirect.html")
    
    tester = db.session.query(UserDetails).filter_by(email=session['email']).first()

    name = tester.firstname
    surname = tester.surname
    email = tester.email

    phonenum = tester.phonenum
    dob = tester.dob.date()
    address = tester.address

    GPname = tester.GPname
    GPsurname=tester.GPsurname
    GPcode = tester.GPcode
    GPaddress = tester.GPaddress
    GPnum = tester.GPnum

    puffs = db.session.query(PuffHistory).order_by(PuffHistory.datetaken.desc()).filter_by(user_id=session['id'])

    replacemsg = None
    exceedmsg = None

    #-------------Asthma Log Table-------------
    puffsdict = {
        1 : {
            "time" : "",
            "inhalertype" : "",
            "puffno" : "",
            "dosage" : ""
        },

        2 : {
            "time" : "",
            "inhalertype" : "",
            "puffno" : "",
            "dosage" : ""
        },

        3 : {
            "time" : "",
            "inhalertype" : "",
            "puffno" : "",
            "dosage" : ""
        },

        4 : {
            "time" : "",
            "inhalertype" : "",
            "puffno" : "",
            "dosage" : ""
        },

        5 : {
            "time" : "",
            "inhalertype" : "",
            "puffno" : "",
            "dosage" : ""
        }
    }   

    if puffs.count() != 0:
        for i in range(0,puffs.count()):
            if i > 4:
                #As table cannot go more than 5
                break
            if puffs[i] is not None:
                lastpuff = datetime.now().date()-(puffs[i].datetaken.date())
                if lastpuff == timedelta(days=0):
                    #Display in hours ago
                    time1 = datetime.now().time()
                    time2 = puffs[i].timetaken.time()
                    timediff = datetime.now() - datetime.combine(datetime.today(), time2)
                    timediff = str(timediff.seconds//3600) + " hours ago"

                else:
                    #Display in days ago
                    timediff = str(abs(lastpuff))[0] + " days ago"
                puffsdict[i+1]["time"] = timediff
                puffsdict[i+1]["inhalertype"] = str(puffs[i].inhalertype)
                puffsdict[i+1]["puffno"] = str(puffs[i].puffno)
                puffsdict[i+1]["dosage"] = str(puffs[i].dosageamt)
            else:   
                pass

    #--------------Asthma Streak-------------
    #Check if puff happened in the past 24 hours, 
    #true: count total number of puffs
    #else: 0
    streak = 0

    puffs = db.session.query(PuffHistory).order_by(PuffHistory.datetaken.desc()).filter_by(user_id=session['id'])

    if puffs.count() != 0:
        lastpuff = (puffs[0].datetaken.date())-datetime.now().date()

        if lastpuff == timedelta(days=0):
            streak += 1

            for i in range(1, puffs.count()):
                delta = (puffs[i].datetaken.date())- puffs[i-1].datetaken.date()
                if abs(delta) <= timedelta(days=1):
                    streak += 1
                else:
                    break
        else:
            streak = 0
    
    #-----------When to get a new inhaler--------------
            #If for a specific name of inhaler, the number of puffs
            #If it exceeds an amount, put a suggestion to replace the users inhalers
    if puffs.count() != 0:
        totaldose = 0
        replace = ""
        puffs = db.session.query(PuffHistory).order_by(PuffHistory.medname.desc()).filter_by(user_id=session['id']) 
        #Puffs filtered by the medicine name
        puffname = puffs.first().medname
        for i in range(0,puffs.count()):
            if puffs[i].medname == puffname and puffs[i].medname != "":
                totaldose += int(puffs[i].puffno)
                if totaldose >= 200:
                    if puffname not in replace:
                        replace += str(puffname) + ", "  
            elif  i<puffs.count() and puffs[i].medname != puffname and puffs[i].medname != "":
                puffname = puffs[i].medname
                totaldose = 0
                totaldose += int(puffs[i].puffno)
                if totaldose >= 200:
                    if puffname not in replace:
                        replace += str(puffname) + ", "  
            elif i == puffs.count():
                break

        replace = replace[0:-2]                
        if len(replace) != 0 :
            replacemsg = f"You may need to replace these inhalers : {replace}"
            
    #---------------If taking too many-------------------
            #Find number of puffs x the number of entries in a specific day
            #If it exceeds 4 for reliever, combination or long-acting, suggest you may be taking too many
    puffs = db.session.query(PuffHistory).filter_by(user_id=session['id'])
    if puffs.count() != 0:
        puffsfilt = puffs.filter_by(datetaken=str(datetime.now().date()))
        entries = 0   
        for i in range(0, puffsfilt.count()):
            entries += puffsfilt[i].puffno
            
        if entries > 4:
            exceedmsg = "You may be taking too many puffs for the day, please consult your Doctor for more information."

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
                    GPnum = GPnum,
                    GPaddress = GPaddress,
                    streak = streak,
                    puffs = puffsdict,
                    replacemsg = replacemsg,
                    exceedmsg = exceedmsg)

@bp.route("/update", methods=['POST', 'GET'])
def updatepost():
    if request.method == 'POST' and session['logged_in'] == True:
        user = db.session.query(UserDetails).filter_by(email=session['email']).first()

        phone_number = request.form.get('phone_number')
        dob = request.form.get('dob')
        address = request.form.get('address')
        gp_name = request.form.get('gp_name')
        gp_surname = request.form.get('gp_surname')
        gp_code = request.form.get('gp_code')
        gp_phone = request.form.get('gp_phone_number')
        gp_address = request.form.get('gp_address')

        # if something inputted, normal
        # if empty - forget about it

        if phone_number != "":
            user.phonenum = phone_number

        if dob != "":
            date_format = '%Y-%m-%d'
            date = datetime.strptime(dob,date_format)
            user.dob = date

        if address != "":
            user.address = address

        if gp_name != "":
            user.GPname = gp_name

        if gp_surname != "":
            user.GPsurname = gp_surname

        if gp_code != "":
            user.GPcode = gp_code

        if gp_address != "":
            user.GPaddress = gp_address

        if gp_phone != "":
            user.GPnum = gp_phone

        db.session.commit()
        return redirect("/logbook")
    if request.method == 'GET' and session['logged_in'] == True:
        return render_template('Update_Details.html')
    else:
        return render_template('Update_Details.html')

@bp.route('/test')
def index():
    return render_template('test.html')

@bp.route('/logout')
def logoutview():
    session.pop('logged_in', None)
    return redirect("/")

app = create_app()
db.init_app(app)
bcrypt = Bcrypt(app)
app.secret_key = b'8dh3w90fph#3r'
#ONLY TO BE RUN IF REMAKING DATABASES:
# with app.app_context():
#     db.drop_all()
#     db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0')