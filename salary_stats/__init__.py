from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from flask_migrate import Migrate

# from app.seed import seed_salaries

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_info']['SQLALCHEMY_DATABASE_URI']

print(app.root_path)
import salary_stats.views

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# with app.app_context():
#     from seed import seed_salaries

# def register_commands(app):
#     app.cli.add_command(seed_salaries)



# register_commands(app)

if __name__ == '__main__':
    app.run(debug=True)