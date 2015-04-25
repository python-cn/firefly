# coding=utf-8
'''Define Schema'''

from datetime import datetime

from flask import url_for, g

from firefly.ext import db
from firefly.views.utils import timesince
from .user import User

__all__ = ["Category", "Post", "Video", "Image", "Comment"]


class Category(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    name = db.StringField(max_length=50, required=True, unique=True)
    _slug = db.StringField(max_length=50, unique=True)
    description = db.StringField(max_length=120, required=True)
    priority = db.IntField(default=0)
    posts = db.ListField(db.ReferenceField('Post'))

    def url(self):
        return url_for('category', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        self._slug = '-'.join(filter(lambda x: x, self._slug.split(' ')))

    meta = {
        'indexes': ['-priority', 'name', 'id'],
        'ordering': ['-priority']
    }


class Post(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    title = db.StringField(max_length=255, required=True)
    content = db.StringField(required=True)
    views = db.IntField(default=0)
    # 有了登录系统author就是必选项
    author = db.ReferenceField(User)
    comments = db.ListField(db.ReferenceField('Comment'))
    category = db.ReferenceField(Category)

    def url(self):
        return url_for('post.detail', id=self.id)

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    @property
    def recent_activity_time(self):
        if self.comments:
            activity = self.comments[-1].created_at
        else:
            activity = self.created_at
        return timesince(activity, locale=g.locale)

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
    content = db.StringField(required=True)
    author = db.ReferenceField(User)


class Comment(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    content = db.StringField(verbose_name='Comment', required=True)
    author = db.ReferenceField(User)

    @property
    def post_type(self):
        return self.__class__.__name__
