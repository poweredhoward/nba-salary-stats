import os
import click
from flask.cli import with_appcontext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from flask_migrate import Migrate
# from app.models.salary import Salary
# from app.seed import seed_db

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object("config.Config")

    config = ConfigParser()
    config.read('app/config.ini')


    app.config['SQLALCHEMY_DATABASE_URI'] = config['Database Info']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['Database Info']['SQLALCHEMY_TRACK_MODIFICATIONS']
    # app.config['SQLALCHEMY_ECHO'] = config['Database Info']['SQLALCHEMY_ECHO']




    db.init_app(app)

    # app.cli.add_command(seed_db)

    with app.app_context():
        from . import views  # Import routes
        from .models.salary import Salary
        from .models.stats import Stats
        # from models import salary

        # db.create_all()  # Create database tables for our data models
        migration_dir = os.path.join('app','migrations')
        migrate = Migrate(app, db, directory=migration_dir)
        # register_commands(app)



        return app



# app = create_app()


