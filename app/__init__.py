from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from flask_migrate import Migrate


config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['Database Info']['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


