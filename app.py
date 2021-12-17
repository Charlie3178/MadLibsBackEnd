from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# models
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    template = db.Column(db.Text, nullable=False)

    def __init__(self, template):
        self.template = template