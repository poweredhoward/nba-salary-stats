import os
import click
from flask.cli import with_appcontext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from flask_migrate import Migrate
# from application.models.salary import Salary
# from application.seed import seed_db

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    application = Flask(__name__, instance_relative_config=False)

    config = ConfigParser()
    config.read('app/config.ini')


    application.config['SQLALCHEMY_DATABASE_URI'] = config.get("Database Info", "SQLALCHEMY_DATABASE_URI")
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['Database Info']['SQLALCHEMY_TRACK_MODIFICATIONS']

    db.init_app(application)

    with application.app_context():
        from . import views 
        from .models.salary import Salary
        from .models.stats import Stats

        migration_dir = os.path.join('app','migrations')
        migrate = Migrate(application, db, directory=migration_dir)

        return application


