#Write for form submission
#Write unit test to also see if it exists in the database 
from ..app import UserDetails
from flask_bcrypt import Bcrypt as bcrypt

def test_registration(client, app):
    response = client.post("/signup", data={"First_name":"testname", 
    "Last_name":"testsur",
    "Email_Address":"test@koffing.com",
    "Password":"testpassword", 
    "Confirm_password":"testpassword",
    'sign_up_form': 'Submit'})

    #'sign_up_form': 'Submit'  is present due to the logic for the logbook  
    with app.app_context():
        user = UserDetails.query.filter_by(email="test@koffing.com")
        assert user.count() == 1
        assert user.first().firstname == "testname"
        assert user.first().surname == "testsur"
        assert user.first().email == "test@koffing.com"
        assert bcrypt(app).check_password_hash(user.first().password, 'testpassword') == True