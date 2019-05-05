from flask_sqlalchemy import SQLAlchemy
from camellia.app import app


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nickname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    salt = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.Integer, default=0)
    inviter = db.Column(db.Integer)
    ancetry = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.DateTime)
    avator=db.Column(db.String(256))
    phone=db.Column(db.String(32), unique=True, nullable=False)
    contribute=db.Column(db.Integer, default=0)
    contribute_all=db.Column(db.Integer, default=0)
    description=db.Column(db.String(512))


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    target_id = db.Column(db.Integer)
    target_name = db.Column(db.String(80))
    description = db.Column(db.String(256))
