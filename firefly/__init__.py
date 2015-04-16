# coding=utf-8

from flask import Flask
from flask.ext.mako import render_template, MakoTemplates
from flask.ext.babel import Babel
from flask.ext.cache import Cache
from flask.ext.mongoengine import MongoEngine
from flask_mail import Mail

from firefly import config

app = Flask(__name__)
app.config.from_object(config)
db = MongoEngine(app)
mako = MakoTemplates(app)
cache = Cache(app)
babel = Babel(app)
mail = Mail(app)


def configure_error_handles(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('403.html')

    @app.errorhandler(404)
    def not_found_page(error):
        return render_template('404.html')


def register_blueprints(app):
    from firefly.views import (home, post)
    for i in (home, post):
        app.register_blueprint(i.bp)
#    configure_error_handles(app)


register_blueprints(app)
