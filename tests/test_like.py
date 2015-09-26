# coding: utf-8

from __future__ import absolute_import
import pytest

from flask import url_for
from flask_login import current_user

from firefly.models.user import User
from firefly.models.topic import Category, Post


@pytest.mark.usefixtures('client_class')
class TestLike:

    users = []

    def setup(self):
        c = Category.objects.create(
            name='python', description='描述', _slug='python-slug'
        )
        Post.objects.create(
            title='标题test', content='内容test', category=c
        )

        self.users = []
        for x in range(3):
            self.users.append(
                User.create_user(
                    username='user' + str(x),
                    password='password123',
                    email='user' + str(x) + '@firefly.dev'
                )
            )

    def login(self, email):
        form = {
            'email': email,
            'password': 'password123'
        }
        self.client.post(
            url_for('home.login'), data=form,
            follow_redirects=True
        )
        assert current_user.is_authenticated()

    def test_like(self):
        post = Post.objects.first()
        assert len(post.likes) == 0

        for user in self.users:
            self.login(user.email)
            url = url_for('api.like', id=post.id)
            rv = self.client.put(url)
            assert rv.status_code == 202
        assert len(post.likes) == len(self.users)

        rv = self.client.delete(url, buffered=True)
        assert rv.status_code == 204
        assert len(post.likes) == 2
