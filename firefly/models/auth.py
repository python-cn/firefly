# coding=utf-8
from datetime import datetime
from mongoengine import fields, DENY
from flask import current_app
from flask_babel import gettext as _
from flask_login import LoginManager, login_user
from flask.ext.mako import render_template
from flask_security import (UserMixin, RoleMixin, Security,
                            MongoEngineUserDatastore)

from firefly import db


class Role(db.Document, RoleMixin):
    name = db.StringField(required=True, unique=True, max_length=80)
    description = db.StringField(max_length=255)

    def __unicode__(self):
        return self.name

    meta = {
        'collection': 'role',
        'indexes': ['name'],
    }


class User(db.Document, UserMixin):
    email = db.StringField(unique=True, max_length=255)
    password = db.StringField(max_length=120)
    active = db.BooleanField(default=True)
    confirmed_at = fields.DateTimeField()
    created = fields.DateTimeField(default=datetime.utcnow())
    remember_token = db.StringField(max_length=255)
    authentication_token = db.StringField(max_length=255)
    first_name = db.StringField(max_length=120)
    last_name = db.StringField(max_length=120)
    roles = fields.ListField(
        fields.ReferenceField(Role, reverse_delete_rule=DENY), default=[])

    @property
    def cn(self):
        if not self.first_name or not self.last_name:
            return self.email
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def id(self):
        return self.pk

    @classmethod
    def by_email(cls, email):
        return cls.objects(email=email).first()

    @property
    def gravatar(self):
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        import hashlib
        encoded = hashlib.md5(email).hexdigest()
        return 'https://secure.gravatar.com/avatar/%s.png' % encoded

    def social_connections(self):
        return SocialConnection.objects(user=self)


class SocialConnection(db.Document):
    user = fields.ReferenceField(User)
    provider = db.StringField(max_length=255)
    profile_id = db.StringField(max_length=255)
    username = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    access_token = db.StringField(max_length=255)
    secret = db.StringField(max_length=255)
    first_name = db.StringField(max_length=255, help_text=_(u'First Name'))
    last_name = db.StringField(max_length=255, help_text=_(u'Last Name'))
    cn = db.StringField(max_length=255, help_text=_(u'Common Name'))
    profile_url = db.StringField(max_length=512)
    image_url = db.StringField(max_length=512)

    def get_user(self):
        return self.user

    @classmethod
    def by_profile(cls, profile):
        provider = profile.data['provider']
        return cls.objects(provider=provider, profile_id=profile.id).first()

    @classmethod
    def from_profile(cls, user, profile):
        if user and not user.is_anonymous():
            user = None
        if not user or user.is_anonymous():
            email = profile.data.get('email')
            if not email:
                msg = 'Cannot create new user, authentication provider need provide email'  # noqa
                raise Exception(_(msg))
            conflict = User.objects(email=email).first()
            if conflict:
                msg = 'Cannot create new user, email {} is already used. Login and then connect external profile.'  # noqa
                msg = _(msg).format(email)
                raise Exception(msg)

            now = datetime.now()
            user = User(
                email=email,
                first_name=profile.data.get('first_name'),
                last_name=profile.data.get('last_name'),
                confirmed_at=now,
                active=True,
            )
            user.save()
            login_user(user)

        connection = cls(user=user, **profile.data)
        connection.save()
        return connection

    def __unicode__(self):
        return self.display_name

    meta = {
        'collection': 'socialconnection',
        'indexes': ['user', 'profile_id'],
    }


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
