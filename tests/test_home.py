def test_home(client):
    
    response = client.get("/home")
    info = response.data.decode()  
    
    assert response.status_code == 200
    
    # Test for the presence of the AQI widget
    assert b'<div class="aqi-widget" id="aqiWidget">' in response.data

    # Test for logbook link
    assert '<div id="My_Logbook_">' in info  
    assert '<svg class="Icon_awesome-user-alt"' in info  

    #Logging puffer button, dropdown, input options, and form submission 
    assert b'<form action="/home" method = "POST">' in info
    assert b'<input id="Puff_button"' in info
    assert b'<select id="Inhaler_type"' in info
    assert b'<input id="Number_of_puffs"' in info
    assert b'<input id="Dosage"' in info
    assert b'<input id="Medname"' in info
