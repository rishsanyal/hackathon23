from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
sql_db = SQLAlchemy(app)

class User(sql_db.Model):
    __tablename__ = 'users'
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(80), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class UserProfile(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    user_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('user.id'), unique=True, nullable=False)
    user = sql_db.relationship('User', back_populates='profile')
    full_name = sql_db.Column(sql_db.String(120))
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    phone = sql_db.Column(sql_db.String(120), unique=True, nullable=False)

