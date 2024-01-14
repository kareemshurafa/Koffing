from ..app import PuffHistory,db
from datetime import datetime,timedelta

def test_streak(client,app):
    #Testing if the streak is created by uploading 5 successive puffs
    currenttime = "08:00"

    date_format = '%Y-%m-%d'
    delta = timedelta(1)
    currentdateobj = datetime.strptime(str(datetime.now().date()-timedelta(5)),'%Y-%m-%d')

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

    print(response.data)
    assert b'<span>5!</span>' in response.data

def test_table(client,app):
    #Testing the table records
        #By checking whether the "time ago" is shown on the table
    currenttime = "12:56"

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
    
    response = client.get("/logbook")
    for i in range(1,6):
        currentdateobj = currentdateobj + delta
        currentdate = currentdateobj.strftime(date_format)
        assert bytes(f'<td>{i} days ago</td>','utf-8') in response.data
    #Have to assert the correct format found within the table

def test_presence(client,app):
    response = client.get("/logbook")
    assert b'<img id="puffer_cartoon" src="../static/images/puffer_cartoon.png">' in response.data

def test_logbook(client):
    response = client.get("/logbook")
    info = response.data.decode() #decode binary to string

    assert response.status_code == 200
    def test_web_1920_2(client):
    response = client.get("/web_1920_2")
    info = response.data.decode()  # Decode binary to string

    assert response.status_code == 200
    
    #assertions checking existence of important HTML elements
    assert '<div id="Home">' in info  # Home button or link
    assert '<table id="Component_53__1">' in info  # Table for displaying data
    assert 'First Name: {{first_name}}' in info  # Placeholder for first name
    assert 'Surname: {{surname}}' in info  # Placeholder for surname
    assert 'Email: {{email}}' in info  # Placeholder for email
    assert '<button id="Update_Details_Button"' in info  # Check for Update Details button

    

