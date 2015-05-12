# coding: utf-8 -*-
from __future__ import absolute_import

from flask import url_for
import pytest

from firefly.models.user import User
from firefly.models.topic import Category, Post


@pytest.mark.usefixtures('client_class')
class TestPost:

    def setup(self):
        c = Category.objects.create(
            name=u'python', description=u'描述', _slug=u'python-slug'
        )
        Post.objects.create(
            title=u'标题test', content=u'内容test', category=c
        )

        # login user
        self.username = 'foo'
        self.password = 'foobar'
        self.email = 'foo@bar.com'
        self.user = User.create_user(
            username=self.username, password=self.password,
            email=self.email
        )

    def test_create(self):
        category = Category.objects.first()
        url = url_for('home.create')
        form = {
            'title': '标题',
            'content': '内容喜喜喜喜喜喜',
            'category': category.id,
            'author': self.user.id
        }
        rv = self.client.post(url, data=form)
        assert rv.json['ok'] == 0

        assert Post.objects.count() > 1

    def test_detail(self):
        post = Post.objects.first()
        url = url_for('post.detail', id=post.id)
        rv = self.client.get(url)
        data = rv.get_data().decode('utf-8')
        assert post.title in data
        assert post.content in data

        #    def test_comment(self):
        #        post = Post.objects.first()
        #        url = url_for('post.detail', id=post.id)
        #        form = {
        #            'content': u'评论测试',
        #        }
        #        rv = self.client.post(url, data=form, follow_redirects=False)

        #        assert rv.status_code == 302
        #        assert Comment.objects.count() == 1
        #        assert len(post.comments) == 1
