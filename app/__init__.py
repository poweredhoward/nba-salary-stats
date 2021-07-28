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
    # application.config.from_object("config.Config")

    config = ConfigParser()
    config.read('app/config.ini')

    # print(config.sections())

    # application.config['SQLALCHEMY_DATABASE_URI'] = config['Database Info']['SQLALCHEMY_DATABASE_URI']
    application.config['SQLALCHEMY_DATABASE_URI'] = config.get("Database Info", "SQLALCHEMY_DATABASE_URI")
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['Database Info']['SQLALCHEMY_TRACK_MODIFICATIONS']
    # application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    db.init_app(application)

    # application.cli.add_command(seed_db)

    with application.app_context():
        from . import views  # Import routes
        from .models.salary import Salary
        from .models.stats import Stats
        # from models import salary

        # db.create_all()  # Create database tables for our data models
        migration_dir = os.path.join('app','migrations')
        migrate = Migrate(application, db, directory=migration_dir)
        # register_commands(application)



        return application



# application = create_app()


