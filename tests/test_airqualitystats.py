def test_airqualitystats(client):
    response = client.get("/airqualitystats")
    info = response.data.decode() #decode binary to string

    
    
