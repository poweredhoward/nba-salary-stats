# from app import db
# import os

from flask.cli import with_appcontext

from flask import current_app as app

# app = create_app()

@with_appcontext
def seed_db():
    print("seed starting")