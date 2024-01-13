from ..app import UserDetails,PuffHistory,db
from flask_bcrypt import Bcrypt as bcrypt
from datetime import datetime,timedelta

#Written in form of html submission
currenttime = "12:56"
currentdate = "2024-01-01"

date_format = '%Y-%m-%d'
time_format = '%H:%M'

def test_logging(client,app):
    response = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":123,
                                            "Medname":"Inhaler",
                                            'regpuff': 'Submit'
                                            })
    
    with app.app_context():
        puff = PuffHistory.query.first()
        assert PuffHistory.query.count()==1
        assert puff.datetaken == datetime.strptime(currentdate,date_format)
        assert puff.timetaken == datetime.strptime(currenttime,time_format)
        assert puff.inhalertype == "Reliever"
        assert puff.dosageamt == 12
        assert puff.puffno == 123
        assert puff.medname == "Inhaler"

def test_streak(client,app):
    currenttime = "12:56"
    currentdate = "2024-01-13"

    date_format = '%Y-%m-%d'
    time_format = '%H:%M'
    delta = timedelta(1)
    currentdateobj = datetime.strptime("2024-01-8",'%Y-%m-%d')

    for i in range(0,5):
        currentdateobj = currentdateobj + delta
        currentdate = currentdateobj.strftime(date_format)
        posts = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":123,
                                            "Medname":"Inhaler",
                                            'regpuff': 'Submit'
                                            })
    
    puffs = db.session.query(PuffHistory).order_by(PuffHistory.id.desc())
    response = client.get("/logbook")
    
    with app.app_context():
        assert puffs.count() == 5    

   
    assert b'<span>test</span>' in response.data
    assert b'<span>5!</span>' in response.data

def test_table(client,app):
    currenttime = "12:56"
    currentdate = "2024-01-13"

    date_format = '%Y-%m-%d'
    time_format = '%H:%M'
    delta = timedelta(1)
    currentdateobj = datetime.strptime("2024-01-8",'%Y-%m-%d')

    for i in range(0,5):
        currentdateobj = currentdateobj + delta
        currentdate = currentdateobj.strftime(date_format)
        posts = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":123,
                                            "Medname":"Inhaler",
                                            'regpuff': 'Submit'
                                            })
    
    #Have to assert the correct format found within the table
