import pytest
from flask_sqlalchemy import SQLAlchemy
from ..app import create_app,db
from flask import session
from flask_bcrypt import Bcrypt

@pytest.fixture()
def app():
    #Setting up the app for the test
    app=create_app("sqlite://")
    db.init_app(app)
    bcrypt = Bcrypt(app)
    with app.app_context():
        db.create_all()
    app.secret_key = b'8dh3w90fph#3r'

    print("Creating Database")
    yield app

@pytest.fixture()
def client(app):
    with app.test_client() as testing_client:
        with testing_client.session_transaction() as session:
            session['id'] = 1

        yield testing_client  # Return to caller.


