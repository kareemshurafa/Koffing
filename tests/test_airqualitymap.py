def test_logbook_button(client):
    # Test for the presence of the "My Logbook" button
    response = client.get("/map")
    assert b'<div id="My_Logbook_">' in response.data

def test_air_quality_map_loading(client):
    # Test to ensure the Air Quality Map loads correctly
    response = client.get("/map")
    assert b'<div id="Air_Quality_Map">' in response.data

def test_search_functionality(client):
    # Test to ensure the search box is present and functional
    response = client.get("/map")
    assert b'<input id = "search-box"' in response.data

def test_map_script_loading(client):
    # Test to ensure the map related script is loaded
    response = client.get("/map")
    assert b'src="https://maps.googleapis.com/maps/api/js' in response.data

def test_aqi_widget_display(client):
    # Test for the presence of the AQI widget
    response = client.get("/map")
    assert b'<div class="aqi-widget" id="aqiWidget">' in response.data

def test_settings_accessibility(client):
    # Test for the presence and accessibility of Settings
    response = client.get("/map")
    assert b'<div id="Settings__">' in response.data