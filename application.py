from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


application = Flask(__name__)
ma = Marshmallow(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
# to stop it from giving us warning
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(application)

import Routes