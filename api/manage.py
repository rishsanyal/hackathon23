import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, sql_db


# app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, sql_db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()