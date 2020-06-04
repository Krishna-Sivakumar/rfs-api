from flask import Flask
from models import *
import os, os.path


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hdqjgsykocnmbq:ba5abe0147435d8a43b8e1cc5e710d056ee422a2779231c5e70d61a24bc78284@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d1s0td7d585tps"
    db.init_app(app)
    return app


def init_database(app):
    with app.app_context():
        db.create_all()


app = create_app()
if not os.path.isfile('sqlite:///test.db'):
    init_database(app)
