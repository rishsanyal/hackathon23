import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from app import create_app,sql_db
from flask_migrate import upgrade,migrate,init,stamp
from auth.auth_models import User, UserProfile

from redis_crud import clear_user_info_queue, dummy_populate_oh_queue

# from app import create_app, sql_db


# app.config.from_object(os.environ['APP_SETTINGS'])

# migrate = Migrate(app, sql_db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

def deploy():
	"""Test"""
	print("TEST")
	# app = create_app()
	# app.app_context().push()
	# with app.app_context():
	# 	sql_db.create_all()

	# # migrate database to latest revision
	# init()
	# stamp()
	# migrate()
	# upgrade()

	clear_user_info_queue()
	dummy_populate_oh_queue(1)


if __name__ == '__main__':
	deploy()