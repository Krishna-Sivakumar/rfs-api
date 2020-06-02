from flask import Flask
from models import *
import os, os.path


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    db.init_app(app)
    return app


def init_database(app):
    with app.app_context():
        db.create_all()


app = create_app()
if not os.path.isfile('sqlite:///test.db'):
    init_database(app)
