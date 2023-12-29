def test_home(client):
    #Client used to send simulated requests
    #Have to send a request to the index
    response = client.get("/")
    
    # assert b"<h2 style='color:red'>Hello Koffing! This is the final test!</h2>" in response.data
    assert b"<h2>Hello Koffing! This is the final test!</h2>" in response.data
    #assert used to check if it exists


    #Do form and database submission in this as well

    