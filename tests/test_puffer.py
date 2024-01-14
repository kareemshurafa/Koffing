from ..app import UserDetails,PuffHistory,db
from datetime import datetime

#Written in form of html submission
currenttime = "12:56"
currentdate = "2024-01-01"

date_format = '%Y-%m-%d'
time_format = '%H:%M'

def test_logging(client,app):
    #Testing if asthma puff uploads are working 
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
