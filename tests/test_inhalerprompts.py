#Test to check if message is flashed if the user:
#1. Takes too many doses in a day
#2. Is running out of doses in a day

currenttime = "12:56"
currentdate = "2024-01-01"

date_format = '%Y-%m-%d'
time_format = '%H:%M'

def test_replace(client,app):
    client.post("/home", data = {"Date_taken":currentdate,
                                            "Time_taken":currenttime,                                         
                                            "Inhaler_type":"Reliever",
                                            "Dosage":12,
                                            "Number_of_puffs":123,
                                            "Medname":"Salbutamol",
                                            'regpuff': 'Submit'
                                            })
    
    response = client.get("/logbook")
    
    assert b'<span>You may need to replace your Salbutamol inhaler</span>' in response.data

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
    assert b'<span>You may need to replace your Turbuhaler,Salbutamol inhaler</span>' in response.data