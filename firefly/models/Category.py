# coding=utf-8
'''Define Schema'''

from datetime import datetime

from flask import url_for

from firefly import db

__all__ = ["Category"]


class Category(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    name = db.StringField(max_length=50, required=True, unique=True)
    summary = db.StringField(max_length=120, required=True)
    priority = db.IntField(default=0)
    posts = db.ListField(db.EmbeddedDocumentField('Post'))

    def get_absolute_url(self):
        return url_for('category', kwargs={'name': self.name})

    def __unicode__(self):
        return self.name

    meta = {
        'indexes': ['-priority', 'name', 'id'],
        'ordering': ['-priority']
        }
