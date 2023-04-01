import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from flask_cors import CORS
from worker import celery
from flask_sqlalchemy import SQLAlchemy

## Login libraries
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from flask_login import (
    LoginManager
)


# from flask import (
#     render_template,
#     redirect,
#     flash,
#     session
# )

# from datetime import timedelta
# from sqlalchemy.exc import (
#     IntegrityError,
#     DataError,
#     DatabaseError,
#     InterfaceError,
#     InvalidRequestError,
# )

# from auth.auth_models import User
# from forms import login_form,register_form

# from werkzeug.routing import BuildError

# from redis_worker import redis_db
# from mock import mock_class_info, mock_office_hours_info

# dev_mode = True
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/mydb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)

# sql_db = SQLAlchemy(app)
sql_db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

migrate = Migrate()
bcrypt = Bcrypt()

def actually_create_app():
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    login_manager.init_app(app)
    sql_db.init_app(app)
    migrate.init_app(app, sql_db)
    bcrypt.init_app(app)

    return app

def create_app():
    return actually_create_app()

app = create_app()

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return "TEST"

