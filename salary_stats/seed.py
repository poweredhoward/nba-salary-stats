# from app import db
import os

# from flask.cli import with_appcontext
from app import app


# @with_appcontext
@app.cli.command()
def seed_salaries():
    print("Seeding salaries")