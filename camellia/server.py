#!/usr/bin/python
# coding:utf8
from functools import wraps
from flask import Response
from flask import session
from flask import render_template
from flask import send_from_directory
import logging
from flask import request
from flask import jsonify
from flask import redirect
import base64
import json
import socket
import uuid
import os
from camellia import conf
from camellia.app import app
from camellia.api.utils import require_auth


LOG = logging.getLogger(__name__)


# 读取配置文件
conf.setup()
app.config['SQLALCHEMY_DATABASE_URI'] = conf.CONF.get('database')
# 因为使用了全局变量来保存配置, 需要确保在读取配置文件之后才能加载api的相关模块
from camellia.api.v1.login import app as login_app
app.register_blueprint(login_app)
from camellia.api.v1.user import app as user_app
app.register_blueprint(user_app)

@app.errorhandler(404)
def not_found(error):
        return render_template('404.html'), 404


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('frontend/images', 'favicon.ico')


@app.route('/globals.js')
def send_global_config():
    user_session = session.get('user_session')
    if user_session:
        user = user_session.get('user', {})
    else:
        user = {}
    return render_template('globals.js',
                           id = user.get('id'),
                           username = user.get('username'),
                           nickname = user.get('nickname'),
                           role = user.get('role'),
                           gender = user.get('gender'),
                           code = user.get('code'))

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('frontend/js', path)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('frontend/images', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('frontend/css', path)


@app.route('/skins/<path:path>')
def send_skins(path):
    return send_from_directory('frontend/skins', path)


@app.route('/fonts/<path:path>')
def send_font(path):
    return send_from_directory('frontend/fonts', path)


@app.route('/statics/<path:path>')
def send_statics(path):
    return send_from_directory('frontend/statics', path)


@app.route('/')
def index():
    return redirect('/statics/login.html', code=302)


def main():
    global app
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)
