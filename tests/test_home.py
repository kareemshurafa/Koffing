def test_home(client):
    
    response = client.get("/home")
    
    assert response.status_code == 200
    
    # Test for the presence of the AQI widget
    assert b'<div class="aqi-widget" id="aqiWidget">' in response.data