import pytest
from flask_sqlalchemy import SQLAlchemy
from ..app import create_app,db,session
from flask_bcrypt import Bcrypt

@pytest.fixture()
def app():
    #Setting up the app for the test
    app=create_app("sqlite://")
    db.init_app(app)
    bcrypt = Bcrypt(app)
    with app.app_context():
        db.create_all()

    print("Creating Database")
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


