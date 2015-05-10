# coding=utf-8
from __future__ import absolute_import
from flask import url_for
from flask_login import current_user
import pytest

from firefly.models.user import User
from firefly.views.api.consts import OK


@pytest.mark.usefixtures('client_class')
class TestUser:

    def setup(self):
        self.users = []
        for x in range(3):
            self.users.append(
                User.create_user(
                    username='user' + str(x),
                    password='user' + str(x),
                    email='user' + str(x) + '@a.com'
                )
            )

    def login(self, user_no):
        form = {
            'email': 'user0@a.com',
            'password': 'user0'
        }
        rv = self.client.post(
            url_for('home.login'), data=form,
            follow_redirects=True
        )
        assert current_user.is_authenticated()
        assert url_for('security.logout') in rv.data

    def test_follow_user_api(self):
        # test follow
        self.login(0)
        assert self.users[0].following == []
        url = url_for('api.followuserapi', id=self.users[1].id)
        rv = self.client.put(url)
        assert rv.status_code == 202
        assert self.users[0].following == [self.users[1]]
        assert self.users[1].follower == [self.users[0]]
        assert rv.json['status'] == OK

        # test unfollow
        url = url_for('api.followuserapi', id=self.users[1].id)
        rv = self.client.delete(url)
        assert rv.status_code == 204
        assert self.users[0].following == []
        assert self.users[1].follower == []
        assert rv.json['status'] == OK

    def test_block_user_api(self):
        # test block
        self.login(0)
        assert self.users[0].blocked_user_id == []
        url = url_for('api.blockuserapi', id=self.users[1].id)
        rv = self.client.put(url)
        assert rv.status_code == 202
        assert self.users[0].blocked_user_id == [self.users[1].id]
        assert rv.json['status'] == OK

        # test unblock
        url = url_for('api.blockuserapi', id=self.users[1].id)
        rv = self.client.delete()
        assert rv.status_code == 204
        assert self.users[0].following == []
        assert rv.json['status'] == OK
