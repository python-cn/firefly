# coding=utf-8
'''Define Schema'''

from datetime import datetime

from flask import url_for

from firefly import db


class Post(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    content = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={'id': self.id})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'id'],
        'ordering': ['-created_at']
    }


class Video(Post):
    embed_code = db.StringField(required=True)


class Image(Post):
    image_url = db.StringField(required=True, max_length=255)


class Quote(Post):
    body = db.StringField(required=True)
    author = db.StringField(verbose_name='Author Name', required=True,
                            max_length=255)


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name='Comment', required=True)
    author = db.StringField(verbose_name='Name', max_length=255, required=True)
