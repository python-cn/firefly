# coding=utf-8
'''Define Schema'''

from datetime import datetime

from flask import url_for
from mongoengine import fields, DENY
from werkzeug import security
from flask_babel import gettext as _
from flask_mail import Message
from flask_login import login_user
from flask_security import UserMixin, RoleMixin

from firefly import app, db, mail, redis_store


class Role(db.Document, RoleMixin):
    name = db.StringField(required=True, unique=True, max_length=80)
    description = db.StringField(max_length=255)

    def __str__(self):
        return str(self).encode('utf-8')

    def __unicode__(self):
        return self.name

    meta = {
        'collection': 'role',
        'indexes': ['name'],
    }


class User(db.Document, UserMixin):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    name = db.StringField(max_length=25)
    email = db.StringField(max_length=255)
    encrypted_password = db.StringField(max_length=255)
    current_sign_in_at = db.DateTimeField(default=datetime.utcnow,
                                          required=True)
    last_sign_in_at = db.DateTimeField(default=datetime.utcnow)
    current_sign_in_ip = db.StringField(max_length=255)
    last_sign_in_ip = db.StringField(max_length=255)
    following = db.ListField(db.ReferenceField('User'), default=[])
    follower = db.ListField(db.ReferenceField('User'), default=[])

    active = db.BooleanField(default=True)  # we can deactive spammer.
    confirmed_at = fields.DateTimeField()  # use social provider register at
    created = fields.DateTimeField(default=datetime.utcnow())
    first_name = db.StringField(max_length=120)
    last_name = db.StringField(max_length=120)
    roles = fields.ListField(
        fields.ReferenceField(Role, reverse_delete_rule=DENY), default=[])

    def url(self):
        return url_for('user', kwargs={'name': self.name})

    def avatar(self, size=48):
        return "%s%s.jpg?size=%s".format(app.config['GRAVATAR_BASE_URL'],
                                         self.email_md5, size)

    @staticmethod
    def generate_encrypted_password(password):
        return security.generate_password_hash(app.config['SECRET_KEY'] +
                                               password)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    def reset_password(self):
        redis_store.set(self.name + 'token', self.create_token())
        redis_store.expire(self.name + 'token', 3600)
        msg = Message("Reset your password",
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[self.email])
        msg.body = "link to check token callback"
        mail.send(msg)

    def verify_reset_password_token(self, token):
        if token != redis_store.get(self.name + 'token'):
            return False, 'token expired or wrong'
        else:
            return True, 'success'

    def change_password(self, password, token):
        result = self.verify_reset_password_token(token)
        if result[0]:
            if self.encrypted_password == User.generate_encrypted_password(
                    password):
                return False, 'duplicate password'
            else:
                self.encrypted_password = User.generate_encrypted_password(
                    password)
                self.save()
                redis_store.remove(self.name + 'token')
                return True, 'success'
        else:
            return result

    def __unicode__(self):
        return self.name

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

    def social_connections(self):
        return SocialConnection.objects(user=self)

    meta = {
        'indexes': ['id'],
        'ordering': ['id']
    }


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
            provider = profile.data.get('provider')
            first_name = profile.data.get('first_name')
            last_name = profile.data.get('last_name')
            if provider not in ('Twitter', 'Douban') and not email:
                msg = 'Cannot create new user, authentication provider need provide email'  # noqa
                raise Exception(_(msg))
            if email is None:
                conflict = User.objects(first_name=first_name,
                                        last_name=last_name).first()
            else:
                conflict = User.objects(email=email).first()
            if conflict:
                msg = 'Cannot create new user, email {} is already used. Login and then connect external profile.'  # noqa
                msg = _(msg).format(email)
                raise Exception(msg)

            now = datetime.now()
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
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
