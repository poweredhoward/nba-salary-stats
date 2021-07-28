from flask_migrate import Migrate, MigrateCommand
from app.seed import seed_db

from application import application, db

migrate = Migrate(application, db)

seed = seed_db