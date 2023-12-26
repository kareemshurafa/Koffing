import pytest
from flask import Flask, render_template,request, json, url_for

#####################################################
#Look into app factory?

app = Flask(__name__)
ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hvjmvqxxszylxg:3d1cdb2f1927cdb2ab1dc5e731015a768577b68f1907654be99a76127df98811@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dfuerbg1k2hvm2'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

def test_request_example(client):
    response = client.get("/posts")
    assert b"<h2>Hello, World!</h2>" in response.data

test_request_example(client)

