from flask_migrate import Migrate, MigrateCommand
from app.seed import seed_db

from app import app, db

migrate = Migrate(app, db)

seed = seed_db