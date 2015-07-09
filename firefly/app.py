# coding=utf-8
from __future__ import absolute_import
import os

from flask import Flask, g, request, send_from_directory
from flask_security import MongoEngineUserDatastore
from flask_social_blueprint.core import SocialBlueprint
from flask_wtf.csrf import CsrfProtect

from firefly import config as _config
from firefly.ext import (
    api, babel, cache, db, login_manager, mail, redis_store, security
)
from firefly.models.user import User, SocialConnection, Role
from firefly.utils import send_mail
from firefly.libs.template import render_template


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(_config)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.realpath(config))

    if app.config['DEBUG']:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    api.init_app(app)
    babel.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    redis_store.init_app(app)
    CsrfProtect(app)

    register_auth(app)
    register_hooks(app)
    register_static(app)
    register_blueprints(app)
    configure_error_handles(app)
    plug_to_db(db)

    return app


def register_static(app):
    app.route('/static/<path:filename>')(
        lambda filename: send_from_directory('static', filename))


def register_auth(app):
    def load_user(user_id):
        return User.objects(_id=user_id)

    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = '/login'

    # Setup Flask-Security
    security.init_app(app, MongoEngineUserDatastore(db, User, Role))
    state = app.extensions['security']
    state.send_mail_task(send_mail)
    app.extensions['security'] = state

    SocialBlueprint.init_bp(app, SocialConnection, url_prefix='/_social')


def configure_error_handles(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_page(error):
        return render_template('404.html'), 404


def register_blueprints(app):
    from firefly.views import (home, post, category, api, keyboard, user)
    for i in (home, post, category, api, keyboard, user):
        app.register_blueprint(i.bp)


def register_hooks(app):
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(
            list(app.config['LANGUAGES'].keys())
        ) or app.config['BABEL_DEFAULT_LOCALE']

    @app.before_request
    def before_request():
        g.locale = get_locale()

    @app.context_processor
    def inject_builtin():
        return {
            'hasattr': hasattr,
            'len': len
        }


def plug_to_db(db):
    from firefly.models.utils import dict_filter

    def to_dict(self, *args, **kwargs):
        return dict_filter(self.to_mongo(), *args, **kwargs)
    setattr(db.Document, 'to_dict', to_dict)
