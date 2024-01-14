def test_logbook(client):
    response = client.get("/logbook")
    info = response.data.decode() #decode binary to string

    assert response.status_code == 200

    #assertions checking existence of some elements, mainly HTML
