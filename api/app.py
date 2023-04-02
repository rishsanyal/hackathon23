import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from flask_cors import CORS
from worker import celery
from flask_sqlalchemy import SQLAlchemy

## Login libraries
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from redis_worker import redis_db
from mock import mock_class_info, mock_office_hours_info
from redis_crud import get_students_queue, update_students_queue, delete_students_queue

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

def actually_create_app():
    ## TODO: What is this shit, remove it.
    """Create the app.

    Returns:
        _type_: _description_
    """
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    login_manager.init_app(app)
    sql_db.init_app(app)
    migrate.init_app(app, sql_db)

    bcrypt = Bcrypt(app)
    bcrypt.init_app(app)

    return app

def create_app():
    return actually_create_app()

app = create_app()

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return "TEST"


"""
Redis client
1. Create a queue
2. Populate with mock data for now

API
1. GET queue -> Mock info
2. Delete call queue -> pop from queue
3. POST queue -> Add a user to the queue
"""

# @app.route('/office_hours_students_queue/<string:queue_name>', methods=['GET'])
# def get_office_hours_students_queue(queue_name: str) -> str:
#     curr_student_queue = get_students_queue()
#     return jsonify(curr_student_queue)

# @app.route('/office_hours_students_queue/<string:queue_name>/queue_name<string: user_id>', methods=['DELETE'])
# def delete_office_hours_students_queue(queue_name: str, user_id: str) -> str:
#     curr_student_queue = delete_students_queue(user_id)
#     return jsonify(curr_student_queue)

# # POST queue -> Add a user to the queue
# # @app.route('/office_hours_students_queue', methods=['POST'])
# # def post_office_hours_students_queue() -> str:
# #     curr_student_queue = update_students_queue(user_info)
# #     return jsonify(curr_student_queue)


# @app.route('/office_hours_students_queue/<string:queue_name>/queue_name<string: user_id>', methods=['POST'])
# def update_office_hours_students_queue(queue_name: str, user_id: str) -> str:
#     curr_student_queue = update_students_queue(user_id)
#     return jsonify(curr_student_queue)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
