# coding=utf-8
'''Define Schema'''
from __future__ import absolute_import

from datetime import datetime

from flask import url_for

from firefly.ext import db
from .user import User

__all__ = ["Message"]


class Message(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    content = db.StringField(required=True)
    read = db.BooleanField(default=False)
    sender = db.ReferenceField(User)
    receiver = db.ReferenceField(User)

    def url(self):
        return url_for('post.detail', id=self.id)

    def __unicode__(self):
        return '{}->{}'.format(self.sender.username, self.receiver.username)

    meta = {
        'indexes': ['-created_at', 'id', 'sender', 'receiver'],
        'ordering': ['-created_at']
    }
