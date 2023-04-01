import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from flask_cors import CORS
from worker import celery
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    logout_user,
    login_required,
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

from app import create_app, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

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
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
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
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            sql_db.session.add(newuser)
            sql_db.session.commit()
            flash(f"Account Succesfully created", "success")
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


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    """
    This is the route that will be called by the client to start the task."""
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


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

# @app.route('/class_info', methods=['GET', 'POST'])
# def class_info() -> str:
#     return jsonify(mock_class_info.MOCK_CLASS_INFO)

# @app.route('/office_hours_info', methods=['GET'])
# def get_office_hours_info() -> str:
#     print("test")
#     return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)

# @app.route('/office_hours_info', methods=['POST'])
# def post_office_hours_info() -> str:
#     user_id = request.form.get('user_id')
#     user_info = request.form.get('user_info')
#     class_id = request.form.get('class_id')

#     return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
