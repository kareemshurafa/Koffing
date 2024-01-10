from ..app import UserDetails,PuffHistory,db
from flask_bcrypt import Bcrypt as bcrypt
from datetime import datetime
currenttime = "12:56 PM"
currentdate = "2024/01/01"

date_format = '%Y/%m/%d'
time_format = '%H:%M %p'

def test_logging(client,app):
    
    response = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":123,
                                            "Medname":"Inhaler"
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