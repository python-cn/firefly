# coding=utf-8

from flask import Flask
from flask_mako import render_template, MakoTemplates
from flask_babel import Babel
from flask_cache import Cache
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_mail import Mail

from firefly import config

app = Flask(__name__)
app.config.from_object(config)
db = MongoEngine(app)
redis_store = FlaskRedis(app)
mako = MakoTemplates(app)
cache = Cache(app)
babel = Babel(app)
mail = Mail(app)

if app.config['DEBUG']:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


def register_plug_to_db(db):
    from firefly.models.utils import dict_filter

    def to_dict(self, *args, **kwargs):
        return dict_filter(self.to_mongo(), *args, **kwargs)
    setattr(db.Document, 'to_dict', to_dict)


def configure_error_handles(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('403.html')

    @app.errorhandler(404)
    def not_found_page(error):
        return render_template('404.html')


def register_blueprints(app):
    from firefly.models import auth
    auth.init_app(app)
    from firefly.views import home, post, keyboard, api
    for i in (home, post, keyboard, api):
        app.register_blueprint(i.bp)
    configure_error_handles(app)


def register_login_manager(app):
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        from firefly.models import User
        return User.objects(id=userid).first()


register_blueprints(app)
register_login_manager(app)
register_plug_to_db(db)
