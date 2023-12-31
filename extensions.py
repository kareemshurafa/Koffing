from flask_sqlalchemy import SQLAlchemy
from .app import app

db=SQLAlchemy()
db.init_app(app)
