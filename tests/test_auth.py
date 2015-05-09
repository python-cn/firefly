# coding=utf-8
from __future__ import absolute_import
from flask import url_for
from flask_login import current_user
import pytest

from firefly.models.user import User


@pytest.mark.usefixtures('client_class')
class TestAuth:

    def setup(self):
        self.username = 'foo'
        self.password = 'foobar'
        self.email = 'foo@bar.com'
        User.create_user(
            username=self.username, password=self.password,
            email=self.email
        )

    def test_register(self):
        username = 'foo2'
        email = 'foo2@bar.com'
        password = 'foobar'
        form = {
            'username': username,
            'email': email,
            'password': password
        }
        self.client.post(url_for('home.register'), data=form)
        assert current_user.is_authenticated()

        user = User.objects.get(email=email)
        assert user.check_password(password)

    def login(self):
        form = {
            'email': self.email,
            'password': self.password
        }
        rv = self.client.post(
            url_for('home.login'), data=form,
            follow_redirects=True
        )
        assert current_user.is_authenticated()
        assert url_for('security.logout') in rv.data

    def test_logout(self):
        self.login()
        self.client.get(url_for('security.logout'))
        assert not current_user.is_authenticated()
