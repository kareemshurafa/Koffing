def test_asthmainfo(client):
    response = client.get("/asthmainfo")
    info = response.data.decode() #decode binary to string
    
    #Test if Logbook link exist
    assert b'<div id="My_Logbook_">' in response.data
    
    assert "Asthma is a chronic respiratory disease affecting individuals of all ages. " in info
    assert "Koffing is a web-based app that offers a novel approach to asthma tracking. " in info

    # Test for the presence of specific images
    assert 'src="../static/images/lung.png"' in info
    assert 'src="../static/images/homespage1.png"' in info
    assert 'src="../static/images/homespage2.png"' in info
    
    #Test if page exist
    assert response.status_code == 200
