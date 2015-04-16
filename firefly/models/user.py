# coding=utf-8
'''Define Schema'''

from datetime import datetime
from hashlib import md5

from flask import url_for
from werkzeug import security
from flask_mail import Message

from firefly import app, db, mail


class User(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    name = db.StringField(max_length=25, required=True, unique=True)
    email = db.StringField(max_length=255, required=True, unique=True)
    email_md5 = db.StringField(max_length=255)
    encrypted_password = db.StringField(max_length=255, required=True)
    reset_password_token = db.StringField(max_length=255)
    reset_password_sent_at = db.StringField(max_length=255)  # expire in 1 hour
    current_sign_in_at = db.DateTimeField(default=datetime.utcnow,
                                          required=True)
    last_sign_in_at = db.DateTimeField(default=datetime.utcnow)
    current_sign_in_ip = db.StringField(max_length=255, required=True)
    last_sign_in_ip = db.StringField(max_length=255)
    following = db.ListField(db.EmbeddedDocumentField('User'))
    follower = db.ListField(db.EmbeddedDocumentField('User'))

    def get_absolute_url(self):
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
        self.reset_password_token = self.create_token()
        msg = Message("Reset your password",
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[self.email])
        msg.body = "link to check token callback"
        mail.send(msg)
        self.reset_password_sent_at = datetime.utcnow()

    def verify_reset_password_token(self, token):
        # if the token not expire
        if (datetime.utcnow() - self.reset_password_sent_at) \
                .total_seconds() > 3600:
            return False, 'token expired'
        else:
            if token == self.reset_password_token:
                return True, 'success'
            else:
                return False, 'wrong token'

    def change_password(self, password, token):
        result = self.verify_reset_password_token(token)
        if result[0]:
            if self.encrypted_password == User.generate_encrypted_password(
                    password):
                # can not use the previous password
                return False, 'duplicate password'
            else:
                self.encrypted_password = User.generate_encrypted_password(
                    password)
                return True, 'success'
        else:
            return result

    def clean(self):
        # generate the email_md5 for gravatar
        self.email_md5 = md5(self.email).hexdigest()

    def __unicode__(self):
        return self.name

    meta = {
        'indexes': ['id'],
        'ordering': ['id']
    }
