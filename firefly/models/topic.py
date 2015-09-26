# coding=utf-8
'''Define Schema'''
from __future__ import absolute_import

from datetime import datetime

from flask import url_for, g

from firefly.ext import db
from firefly.views.utils import timesince
from firefly.models.consts import CATEGORY_COLORS
from .user import User
from .like import Likes

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
        return url_for('category.detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        self._slug = '-'.join(filter(lambda x: x, self._slug.split(' ')))

    @property
    def color(self):
        return CATEGORY_COLORS[self.id - 1]

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

    likes = Likes()

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
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    content = db.StringField(verbose_name='Comment', required=True)
    author = db.ReferenceField(User)
    ref_id = db.IntField(default=0)

    likes = Likes()

    @property
    def post_type(self):
        return self.__class__.__name__

    def get_replies(self):
        return Comment.objects.filter(ref_id=self.id)


def get_all_posts():
    posts = Post.objects.all()
    for post in posts:
        yield get_post(post)


def get_post(post):
    id = post.id
    # author = post.author
    category = post.category
    category_name = ''
    category_slug = ''
    category_color = '#999'
    if category is not None:
        category_name = category.name
        category_slug = category.slug
        category_color = category.color
    title = post.title
    replies = len(post.comments)
    views = post.views
    created_at = post.created_at
    activity = post.recent_activity_time
    return (post, id, category, category_name, category_slug, category_color,
            title, replies, views, created_at, activity)
