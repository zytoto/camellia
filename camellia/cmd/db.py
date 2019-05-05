#coding:utf8
from camellia.db.sqlalchemy import db
from camellia.db.sqlalchemy import User

from camellia import utils
from camellia import conf as cfg
import uuid
from datetime import datetime
import sys
from camellia.app import app


cfg.setup()
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.CONF.get('database')


def destroy_db():
    db.drop_all()

def init_db():
    db.create_all() 

    conf = cfg.CONF
    password = conf.get('super_user_password')
    salt = str(uuid.uuid4())

    h_pass = utils.hash_password(password, salt)
    super_user = User(
        username = 'admin',
        nickname = u'超级管理员',
        email=conf.get('super_user_email'),
        password=h_pass,
        salt=salt,
        code='',
        role=0,
        inviter=-1,
        ancetry=-1,
        created_at=datetime.now(),
        gender=0,
        birthday=datetime.now(),
        avator='super_user.png',
        phone=conf.get('super_user_phone'),
        description=u'超级用户'
    )

    db.session.add(super_user)
    db.session.commit()


def main():
    action = 'init'
    if len(sys.argv) > 1:
        action = sys.argv[1]
    if action == 'destroy':
        destroy_db()
    else:
        init_db()
