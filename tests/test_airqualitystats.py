def test_airqualitystats(client):
    response = client.get("/airqualitystats")
    info = response.data.decode() #decode binary to string

    assert response.status_code == 200

    #checking for specific HTML elements 
    assert '<div id="Air_Quality_Stats">' in info  # Check for main div id
    assert '<div id="My_Logbook_">' in info  # Check for Logbook link
    assert '<svg class="Icon_awesome-user-alt"' in info  # Check for SVG icon
    assert '<div id="Asthma_Information">' in info  # Check for Asthma Information link
    assert '<div id="Air_Quality_Info">' in info  # Check for Air Quality Map and Info link
    assert '<div id="AIR_QUALITY_STATISTICS__">' in info  # Check for Air Quality Statistics header


    
    
