import logging
import os
from six.moves import configparser
import six
import yaml


CONF = {
    'super_user_password': 'have fun!!!',
    'super_user_email': 'yo.zed@qq.com',
    'super_user_phone': ' ',
    'avator_store': '',
    'debug': 'False',
    'database': 'sqlite:////tmp/camellia.db'
}

# PRODUCTS = {}


def setup():
    global CONF
    global PRODUCTS
    if 'VIRTUAL_ENV' in os.environ:
        config_path = os.path.join(os.environ['VIRTUAL_ENV'],
                                   'etc/camellia/camellia.conf')
    elif os.path.isfile('/etc/camellia/camellia.conf'):
        config_path = '/etc/camellia/camellia.conf'
    elif os.path.isfile('/usr/local/etc/camellia/camellia.conf'):
        config_path = '/usr/local/etc/camellia/camellia.conf'
    else:
        config_path = None
    if config_path:
        if six.PY2:
            ConfigParser = configparser.SafeConfigParser
        else:
            ConfigParser = configparser.ConfigParser

        parser = ConfigParser(CONF)
        parser.read(config_path)

        for name in CONF.keys():
            CONF[name] = parser.get('DEFAULT', name)

    logging_level = logging.DEBUG if CONF['debug'] else logging.INFO
    logging.basicConfig(level=logging_level,
                        format='%(filename)s: '
                        '%(levelname)s: '
                        '%(funcName)s(): '
                        '%(lineno)d:\t'
                        '%(message)s')


