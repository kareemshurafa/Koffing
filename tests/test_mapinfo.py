def test_mapinfo(client):
    response = client.get("/mapinfo")
    # Test for the presence of the "My Logbook" button
    assert b'<div id="My_Logbook_">' in response.data
    
    # Test to ensure the Air Quality Map loads correctly
    assert b'<div id="Air_Quality_Map">' in response.data
    
    # Test to ensure the map related script is loaded
    assert b'src="https://maps.googleapis.com/maps/api/js' in response.data
    
    # Test for the presence of the AQI widget
    assert b'<div class="aqi-widget" id="aqiWidget">' in response.data
    
    # Test for the presence of the chart
    assert b'<div id = "aqiChart">' in response.data
    
    assert response.status_code == 200
