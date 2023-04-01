from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import os
import sys

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)



# # init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db:5432/mydb'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     CORS(app)

#     sql_db = SQLAlchemy(app)
#     sql_db.init_app(app)

#     # blueprint for auth routes in our app
#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     # blueprint for non-auth parts of app
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app