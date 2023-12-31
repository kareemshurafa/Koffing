#Write for form submission
#Write unit test to also see if it exists in the database 
from Koffing.app import UserDetails
from flask_bcrypt import Bcrypt as bcrypt

def test_registration(client, app):
    response = client.post("/logbook", data={"First_name":"testname", 
    "Last_name":"testsur",
    "Email_Address":"test@koffing.com",
    "Password":"testpassword", 
    'sign_up_form': 'Submit'})

    #'sign_up_form': 'Submit'  is present due to the logic for the logbook  
    with app.app_context():
        assert UserDetails.query.count() == 1
        assert UserDetails.query.first().firstname == "testname"
        assert UserDetails.query.first().surname == "testsur"
        assert UserDetails.query.first().email == "test@koffing.com"
        assert bcrypt(app).check_password_hash(UserDetails.query.first().password, 'testpassword') == True
