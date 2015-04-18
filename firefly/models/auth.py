# coding=utf-8
from flask import current_app
from flask_login import LoginManager
from flask_mako import render_template
from flask_security import Security, MongoEngineUserDatastore

from firefly import db
from firefly.models.user import User, SocialConnection, Role


def load_user(user_id):
    return User.objects(_id=user_id)


def send_mail(msg):
    mail = current_app.extensions.get('mail')
    mail.send(msg)


def init_app(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    login_manager.login_view = '/login'

    # Setup Flask-Security
    security = Security()
    security = security.init_app(app, MongoEngineUserDatastore(db, User, Role))
    security.send_mail_task(send_mail)

    from flask_social_blueprint.core import SocialBlueprint
    SocialBlueprint.init_bp(app, SocialConnection, url_prefix='/_social')

    state = app.extensions['security']
    state.render_template = render_template
    app.extensions['security'] = state
