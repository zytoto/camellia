# coding:utf8
from functools import wraps
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response
from flask import session
import json
import logging
import time


LOG = logging.getLogger(__name__)


def abort(http_status_code, **kwargs):
    """Raise a HTTPException for the given http_status_code. Attach any keyword
    arguments to the exception for later processing.
    """
    # noinspection PyUnresolvedReferences
    e = HTTPException(
        response=Response(
            json.dumps(kwargs),
            http_status_code,
            [('Content-Type', 'application/json')]
        )
    )
    e.code = http_status_code
    raise e


def response(data, http_status_code=200):

    return Response(
        json.dumps(data),
        http_status_code,
        [('Content-Type', 'application/json')]
    )


def make_user_session(user):
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'email': user.email,
            'code': user.code,
            'role': user.role,
            'inviter': user.inviter,
            'ancetry': user.ancetry,
            'gender': user.gender,
            'phone': user.phone,
            'contribute': user.contribute,
            'contribute_all': user.contribute_all
        },
        'created_at': time.time(),
        'expire_seconds': 15*60
    }


def refresh_session():
    user_session = session.get('user_session')
    user_session.created_at = time.time()


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check auth
        user_session = session.get('user_session')
        if user_session is None:
            abort(401, msg='您需要登录才能进行当前的操作')
        now = time.time()
        delta = now - user_session['created_at']
        if delta > user_session['expire_seconds']:
            session['user_session'] = None
            abort(401, msg='您的登录已经超时，请重新登录')

        # 已登录用户, 更新session
        user_session['created_at'] = time.time()

        # 执行api
        return f(*args, **kwargs)
    return decorated
