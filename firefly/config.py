# coding=utf-8
from plim import preprocessor

SECRET_KEY = '\x97\xfa%\xab\xd2\xc2\xf8\xfc\xef\xaeTKDk\xc0\xe1//($\xc7\xc0'

# plim
MAKO_DEFAULT_FILTERS = ['decode.utf_8', 'h']
MAKO_PREPROCESSOR = preprocessor
MAKO_TRANSLATE_EXCEPTIONS = False

# mongodb
MONGODB_SETTINGS = {
    'db': 'test',
    'username': '',
    'password': '',
    'host': '127.0.0.1',
    'port': 27017
}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# redis cache
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = ''
