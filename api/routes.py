import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from flask_cors import CORS
from worker import celery
from flask_sqlalchemy import SQLAlchemy
from redis_crud_helper import add_student_info
from redis_crud import get_students_oh_queue, \
add_student_to_oh_queue, delete_student_from_oh_queue, \
add_student_notification_office_hours, get_all_student_notification_office_hours

from flask_bcrypt import bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    logout_user,
    login_required,
    login_user
)


from flask import (
    render_template,
    redirect,
    flash,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)


from auth.auth_models import User
from forms import login_form, register_form

from werkzeug.routing import BuildError

from redis_worker import redis_db
from mock import mock_class_info, mock_office_hours_info

from app import create_app, login_manager, sql_db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

## CELERY API JOBS
@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    return "Ok"


@app.route('/office_hours_info', methods=['GET'])
def get_office_hours_info() -> str:
    print("test")
    return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user.password == form.pwd.data:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            # email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                # email=email,
                password=pwd,
            )

            sql_db.session.add(newuser)
            sql_db.session.commit()
            flash(f"Account Succesfully created", "success")

            ## Add user info to redis
            add_student_info(int(newuser.id), newuser.username)

            return redirect(url_for("login"))

        except InvalidRequestError:
            sql_db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            sql_db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            sql_db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            sql_db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            sql_db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            sql_db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/notification_office_hours', methods=['POST'])
def post_notification_office_hours() -> str:
    """Add student for office hours notifications"""

    user_id = request.args.get('user_id')
    office_hours_id = request.args.get('office_hours_id')
    class_id = request.args.get('class_id')

    if not user_id or not office_hours_id or not class_id:
        return jsonify("Missing parameters"), 400

    return jsonify(add_student_notification_office_hours(user_id, office_hours_id, class_id))


@app.route('/notification_office_hours', methods=['GET'])
def get_all_notification_oh() -> str:
    return jsonify(get_all_student_notification_office_hours())

@app.route('/notification_office_hours', methods=['POST'])
def post_notification_office_hours_turn() -> str:
    """Add student for office hours notifications"""

    user_id = request.args.get('user_id')
    office_hours_id = request.args.get('office_hours_id')
    class_id = request.args.get('class_id')

    if not user_id or not office_hours_id or not class_id:
        return jsonify("Missing parameters"), 400

    return jsonify(add_student_notification_office_hours(user_id, office_hours_id, class_id))


# @app.route('/check/<string:task_id>')
# def check_task(task_id: str) -> str:
#     res = celery.AsyncResult(task_id)
#     if res.state == states.PENDING:
#         return res.state
#     else:
#         return str(res.result)


# @app.route('/health_check')
# def health_check() -> Response:
#     return jsonify("OK")

# @app.route('/test/<string:param1>')
# def test(param1: str) -> str:
#     redis_db.set('param1', param1)
#     redis_db.set('param2', 'param2')
#     print("test2")
#     return jsonify("OK")

@app.route('/class_info', methods=['GET', 'POST'])
def class_info() -> str:
    return jsonify(mock_class_info.MOCK_CLASS_INFO)

# @app.route('/office_hours_info', methods=['GET'])
# def get_office_hours_info() -> str:
#     print("test")
#     return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)

@app.route('/office_hours_info', methods=['POST'])
def post_office_hours_info() -> str:
    """Add office hours notification to the queue"""

    user_id = request.form.get('user_id')
    user_info = request.form.get('user_info')
    class_id = request.form.get('class_id')

    return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)

@app.route('/get_students_queue', methods=['GET'])
def get_students_queue() -> str:
    """Get students queue for office hours"""""

    office_hours_id = request.args.get('office_hours_id')

    if not office_hours_id:
        return jsonify("Missing parameters"), 400

    return jsonify(get_students_oh_queue(office_hours_id))

# # @app.route('/update_students_queue', methods=['POST'])
# # def update_students_queue() -> str:
# #     user_id = request.args.get('user_id')
# #     office_hours_id = request.args.get('office_hours_id')

# #     add_student_to_oh_queue(user_id, office_hours_id)
# #     return jsonify("Student add to OH queue.")

# #     if not office_hours_id:
# #         return jsonify("Missing parameters"), 400

#     return jsonify(get_students_oh_queue(office_hours_id))

@app.route('/update_students_queue', methods=['POST'])
def update_students_queue() -> str:
    """Add students to the OH queue"""
    user_id = request.args.get('user_id')
    office_hours_id = request.args.get('office_hours_id')

    if not user_id or not office_hours_id:
        return jsonify("Missing parameters"), 400

    add_student_to_oh_queue(user_id, office_hours_id)
    return jsonify("Student add to OH queue.")

@app.route('/delete_students_queue', methods=['DELETE'])
def delete_student_from_queue() -> str:
    """Delete the student from office hours queue.
       We could use the student ID to double check if the student is in the queue.
    """

    office_hours_id = request.args.get('office_hours_id')

    if not office_hours_id:
        return jsonify("Missing parameters"), 400

    return jsonify(delete_student_from_oh_queue(office_hours_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
