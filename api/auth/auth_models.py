from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app import app, sql_db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
# sql_db = SQLAlchemy(app)

class User(sql_db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(80), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class UserProfile(sql_db.Model):
    __tablename__ = 'userprofile'
    __table_args__ = {'extend_existing': True}
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    full_name = sql_db.Column(sql_db.String(120))
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    phone = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    # biography = sql_db.Column(sql_db.String(120), unique=True, nullable=False)

    def __init__(self, full_name, email, phone, bio=""):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.bio = bio


with app.app_context():
    sql_db.create_all()

    sql_db.session.add(User('admin', 'admin@example.com'))
    sql_db.session.add(User('guest', 'guest@example.com'))
    sql_db.session.commit()

    users = User.query.all()
    print(users)