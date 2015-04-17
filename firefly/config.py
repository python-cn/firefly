# coding=utf-8
'''
firefly settings
'''
from __future__ import print_function
from plim import preprocessor

SECRET_KEY = 'you need modify this into local_settings.py'

DEBUG = False

# plim
MAKO_DEFAULT_FILTERS = ['decode.utf_8', 'h']
MAKO_PREPROCESSOR = preprocessor
MAKO_TRANSLATE_EXCEPTIONS = False

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# available languages
LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese'
}

BABEL_DEFAULT_LOCALE = 'zh'

GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
DEAFULT_AVATAR = 'your default avatar'

LOGIN_DISABLED = False
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_DEFAULT_REMEMBER_ME = True
CSRF_ENABLED = True

try:
    from local_settings import *  # noqa
except ImportError:
    print('You need rename local_config.py.example to local_config.py, '
          'then update your settings')
    raise
