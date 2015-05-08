from __future__ import absolute_import
# coding=utf-8
from flask import current_app
from flask_babel import Babel
from flask_cache import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_mako import MakoTemplates
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_restful import Api
from flask_security import Security
from werkzeug.local import LocalProxy

api = Api()
babel = Babel()
cache = Cache()
db = MongoEngine()
login_manager = LoginManager()
mail = Mail()
mako = MakoTemplates()
redis_store = FlaskRedis()
security = Security()

logger = LocalProxy(lambda: current_app.logger)
