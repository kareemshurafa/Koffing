import pytest

from flask_sqlalchemy import SQLAlchemy
from Koffing import create_app

@pytest.fixture()
def app():
    #Setting up the app for the test
    app=create_app("sqlite://")
    # db=SQLAlchemy(app)
    
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


