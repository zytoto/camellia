# coding:utf8
import logging
import base64
from flask import Blueprint
from flask import session
from flask import request
from camellia.api.utils import abort
from camellia.api.utils import response
from camellia.api.utils import make_user_session
from camellia.db.sqlalchemy import User
from camellia.utils import hash_password
import sqlite3
from werkzeug.exceptions import HTTPException


app = Blueprint('login', __name__, url_prefix='/api/v1/login')
LOG = logging.getLogger(__name__)


@app.route('/', methods=['POST'])
def login():
    try:
        data = request.get_json()
        LOG.debug('request login: {}'.format(data))
        query = data.get('query')
        orig = None
        if query:
            params = query.split('&')
            for param in params:
                if param[0:5] == 'orig=':
                    try:
                        orig = base64.urlsafe_b64decode(str(param[5:])).decode('utf-8')
                    except Exception as e:
                        LOG.exception(e)
        LOG.debug('login from orig: {}'.format(orig))

        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            abort(401, msg='用户不存在或者密码错误')
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(401, msg='用户不存在或者密码错误')
        salt = user.salt

        pwd = hash_password(password, salt)
        if pwd != user.password:
            abort(401, msg='用户不存在或者密码错误')
        user_session = make_user_session(user)
        session['user_session'] = user_session

        if not orig:
            if user.role == 0:
                # super user
                orig = '/statics/user-list.html'
            elif user.role == 1:
                # admin user
                orig = '/statics/user-info.html'
            elif user.role == 2:
                # normal user
                orig = '/statics/user-info.html'
            else:
                # unknow user
                orig = '/statics/user-info.html'
        return response(
            {
                'msg': '登录成功',
                'orig': orig
            }
        )
    except HTTPException as e:
        LOG.exception(e)
        raise e
    except sqlite3.OperationalError as e:
        LOG.exception(e)
        abort(401, msg='用户不存在或者密码错误')
    except Exception as e:
        LOG.exception(e)
        abort(500, msg=str(e))


@app.route('/', methods=['DELETE'])
def logout():
    session['user_session'] = None
    return response({
        'state': "success"
    })
