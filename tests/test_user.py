# coding=utf-8
from __future__ import absolute_import
from flask import url_for
from flask_login import current_user
import pytest

from firefly.six import unicode
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

    def test_user_settings(self):
        LOCATION = 'Beijing'
        WEBSITE = 'http://firefly.dev'
        GITHUB_ID = 'firefly'

        self.login(0)
        url = url_for('user.settings')
        assert self.users[0].location is None
        assert self.users[0].website is None
        assert self.users[0].github_id is None

        form = {
            'location': LOCATION,
            'website': WEBSITE,
            'github_id': GITHUB_ID
        }
        rv = self.client.post(url, data=form)
        assert rv.status_code == 302

        user = User.objects.filter(id=self.users[0].id).first()
        assert user
        assert user.location == LOCATION
        assert user.website == WEBSITE
        assert user.github_id == GITHUB_ID

    def test_follow_user_api(self):
        # test follow
        self.login(0)
        assert self.users[0].following == []
        url = url_for('api.followuserapi', id=self.users[1].id)
        rv = self.client.put(url, buffered=True)
        assert rv.status_code == 202
        assert rv.json['status'] == OK
        self.users[0].reload()
        self.users[1].reload()
        assert self.users[0].following == [self.users[1]]
        assert self.users[1].follower == [self.users[0]]

        # test unfollow
        url = url_for('api.followuserapi', id=self.users[1].id)
        rv = self.client.delete(url, buffered=True)
        assert rv.status_code == 204
        self.users[0].reload()
        self.users[1].reload()
        assert self.users[0].following == []
        assert self.users[1].follower == []

    def test_block_user_api(self):
        # test block
        self.login(0)
        assert self.users[0].blocked_user_id == []
        url = url_for('api.blockuserapi', id=self.users[1].id)
        rv = self.client.put(url, buffered=True)
        assert rv.status_code == 202
        assert rv.json['status'] == OK
        self.users[0].reload()
        assert self.users[0].blocked_user_id == [unicode(self.users[1].id)]

        # test unblock
        url = url_for('api.blockuserapi', id=self.users[1].id)
        rv = self.client.delete(url, buffered=True)
        assert rv.status_code == 204
        self.users[0].reload()
        assert self.users[0].following == []
