from ..app import UserDetails
from datetime import datetime

def test_updatingsome(client,app):
    dobobj = datetime.strptime("2024-01-8",'%Y-%m-%d')
    date_format = '%Y-%m-%d'
    dob = dobobj.strftime(date_format)
    post =client.post("/update", data={"dob": dob
           })
    
    with app.app_context():
        user = UserDetails.query.filter_by(email="test@test.com")
        assert user.first().dob == datetime(2024, 1, 8, 0, 0)
        assert user.first().GPname == None  
    #Assert that the data was updated in the table