#Test to check if message is flashed if the user:
#1. Takes too many doses in a day
#2. Is running out of doses in a day
from datetime import datetime

currenttime = "12:56"
currentdate = datetime.now().date()

date_format = '%Y-%m-%d'
time_format = '%H:%M'

currentdate = currentdate.strftime(date_format)
def test_replace(client,app):
    post = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":300,
                                            "Number_of_puffs":500,
                                            "Medname": 'Salbutamol',
                                            'regpuff': 'Submit'
                                            })
    
    post = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":300,
                                            "Medname": 'Salbutamol',
                                            'regpuff': 'Submit'
                                            })
    
    post = client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":300,
                                            "Medname": "Turbuhaler",
                                            'regpuff': 'Submit'
                                            })
    
    response = client.get("/logbook")

    assert b'You may need to replace these inhalers : Turbuhaler, Salbutamol' in response.data

def test_replacemultiple(client,app):
    client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":200,
                                            "Number_of_puffs":100,
                                            "Medname":"Salbutamol",
                                            'regpuff': 'Submit'
                                            })
    client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":50,
                                            "Number_of_puffs":100,
                                            "Medname":"Turbuhaler",
                                            'regpuff': 'Submit'
                                            })
    
    client.post("/home", data = {"Date_taken":currentdate,
                                        "Time_taken":currenttime,                                         
                                        "Inhaler_type":"Reliever",
                                        "Dosage":10,
                                        "Number_of_puffs":150,
                                        "Medname":"Salbutamol",
                                        'regpuff': 'Submit'
                                        })
                                        

    client.post("/home", data = {"Date_taken":currentdate,
                                        "Time_taken":currenttime,                                         
                                        "Inhaler_type":"Reliever",
                                        "Dosage":12,
                                        "Number_of_puffs":150,
                                        "Medname":"Turbuhaler",
                                        'regpuff': 'Submit'
                                        })  
    
    response = client.get("/logbook")
    assert b'You may need to replace these inhalers : Turbuhaler, Salbutamol' in response.data

def test_exceed(client,app):
    currentdate = datetime.now().date()
    date_format = '%Y-%m-%d'

    currentdate = currentdate.strftime(date_format)

    client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":200,
                                            "Number_of_puffs":2,
                                            "Medname":"Salbutamol",
                                            'regpuff': 'Submit'
                                            })
    client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":50,
                                            "Number_of_puffs":3,
                                            "Medname":"Turbuhaler",
                                            'regpuff': 'Submit'
                                            })
    
    client.post("/home", data = {"Date_taken":currentdate,
                                        "Time_taken":currenttime,                                         
                                        "Inhaler_type":"Reliever",
                                        "Dosage":10,
                                        "Number_of_puffs":4,
                                        "Medname":"Salbutamol",
                                        'regpuff': 'Submit'
                                        })
                                        
    client.post("/home", data = {"Date_taken":currentdate,
                                        "Time_taken":currenttime,                                         
                                        "Inhaler_type":"Reliever",
                                        "Dosage":12,
                                        "Number_of_puffs":2,
                                        "Medname":"Turbuhaler",
                                        'regpuff': 'Submit'
                                        })  
    
    response = client.get("/logbook")
    print(response.data)
    assert b'You may be taking too many puffs for the day, please consult your Doctor for more information.' in response.data