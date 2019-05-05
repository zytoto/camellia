# coding:utf8
import logging
from flask import Blueprint
from flask import session
from flask import request
from camellia.api.utils import abort
from camellia.api.utils import response
from camellia.api.utils import require_auth
from camellia.db.sqlalchemy import User
from camellia.db.sqlalchemy import db
from camellia.utils import hash_password
import sqlite3
from werkzeug.exceptions import HTTPException
import uuid
import random
import string
from datetime import datetime


app = Blueprint('user', __name__, url_prefix='/api/v1/user')
LOG = logging.getLogger(__name__)


@app.route('/', methods=['POST'])
def create_user():
    try:
        user_session = session['user_session']
        data = request.get_json()
        LOG.debug('request login: {}'.format(data))

        action = data.get('action')
        if action is None:
            # 创新新用户
            kind = 1
            target_role = 2
            code = data.get('code')
            if code is None:
                abort(400, msg='无效的邀请码')

            user_inviter = User.query.filter_by(code=code).first()
            if user_inviter is None:
                abort(400, msg='无效的邀请码')
            inviter_id = user_inviter.id
            ancetry_id = user_inviter.ancetry
        else:
            kind = 2
            inviter_id = user_session['user']['id']
            role = user_session['user']['role']
            target_role = int(data.get('role'))
            if role == 0:
                ancetry_id = user_session['user']['id']
                if target_role != 2 and target_role != 1:
                    abort(403, msg='您无权进行此操作, 您不能创建此种角色的用户')
            elif role == 1:
                ancetry_id = user_session['user']['ancetry']
                if target_role != 2:
                    abort(403, msg='您无权进行此操作, 您不能创建此种角色的用户')
            user_inviter = User.query.filter_by(id=inviter_id).first()

        salt = str(uuid.uuid4())
        password = data.get('password')
        h_pass = hash_password(password, salt)

        # TODO 插入日志

        # TODO 表单验证
        code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        user = User(
            username=data.get('username'),
            nickname=data.get('username'),
            email=data.get('email'),
            password=h_pass,
            salt=salt,
            code=code,
            role=target_role,
            kind=kind,
            inviter=inviter_id,
            ancetry=ancetry_id,
            created_at=datetime.now(),
            gender=int(data.get('gender')),
            birthday=datetime.now(),
            avator='super_user.png',
            phone=data.get('phone'),
            description=data.get('description')
        )

        db.session.add(user)
        if action is None:
            user_inviter.contribute = user_inviter.contribute + 1
        db.session.commit()

        return response(
            {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email,
                    'code': user.code,
                    'role': user.role,
                    'kind': user.kind,
                    'inviter': user.inviter,
                    'gender': user.gender,
                    'avator': user.avator,
                    'phone': user.phone,
                    'contribute': user.contribute,
                    'contribute_all': user.contribute_all,
                    'description': user.description
                }
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


@app.route('/', methods=['GET'])
@require_auth
def get_user_list():
    try:
        page = int(request.args.get('page'))
        pagesize = int(request.args.get('pagesize'))
        mode = request.args.get('mode', 'self')

        user_session = session['user_session']
        inviter = request.args.get('user_id', user_session['user']['id'])
        role = user_session['user']['role']
        if mode == 'all':
            if role != 0:
                abort(403, msg='您无权进行此操作')
            users = User.query.slice(page*pagesize, pagesize)
            page_total = int((User.query.count()+pagesize)/pagesize)
        else:
            users = User.query.filter_by(inviter=inviter).slice(page*pagesize, pagesize)
            page_total = int((User.query.filter_by(inviter=inviter).count()+pagesize)/pagesize)

        result = {
            'page_total': page_total,
            'users': []
        }

        for user in users:
            result['users'].append(
                {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email,
                    'code': user.code,
                    'role': user.role,
                    'kind': user.kind,
                    'inviter': user.inviter,
                    'gender': user.gender,
                    'avator': user.avator,
                    'phone': user.phone,
                    'birthday': str(user.birthday),
                    'contribute': user.contribute,
                    'contribute_all': user.contribute_all,
                    'description': user.description
                }
            )
        return response(result)
    except HTTPException as e:
        LOG.exception(e)
        raise e
    except sqlite3.OperationalError as e:
        LOG.exception(e)
        abort(401, msg='用户不存在或者密码错误')
    except Exception as e:
        LOG.exception(e)
        abort(500, msg=str(e))


@app.route('/<user_id>/detail', methods=['GET'])
@require_auth
def get_user_detail(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()

        result = {
            'user': {
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'email': user.email,
                'code': user.code,
                'role': user.role,
                'kind': user.kind,
                'inviter': user.inviter,
                'gender': user.gender,
                'avator': user.avator,
                'phone': user.phone,
                'birthday': str(user.birthday),
                'description': user.description,
                'contribute_all': user.contribute_all,
                'contribute': user.contribute
            }
        }

        return response(result)
    except HTTPException as e:
        LOG.exception(e)
        raise e
    except sqlite3.OperationalError as e:
        LOG.exception(e)
        abort(401, msg='用户不存在或者密码错误')
    except Exception as e:
        LOG.exception(e)
        abort(500, msg=str(e))
