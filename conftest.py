# coding=utf-8
from __future__ import absolute_import

from flask import url_for
from flask_login import current_user
import pytest

from firefly.app import create_app
from firefly.ext import db
from firefly.models.user import User


@pytest.fixture
def app(request):
    app = create_app('tests/settings.py')
    db_name = app.config['MONGODB_SETTINGS']['db']

    def cleanup():
        db.connection.drop_database(db_name)
    request.addfinalizer(cleanup)
    return app


@pytest.fixture
def client_class(request, client):
    def login(cls):
        user = User.objects.filter(email='foo@bar.com').first()
        if user is None:
            user = User.create_user('foo', 'foo@bar.com', 'foobar')
        else:
            user.set_password('foobar')
            user.save()

        form = {
            'email': 'foo@bar.com',
            'password': 'foobar',
        }
        rv = client.post(
            url_for('home.login'), data=form,
            follow_redirects=True
        )
        assert current_user.is_authenticated()
        assert url_for('security.logout') in rv.data

    if request.cls is not None:
        request.cls.client = client
        request.cls._login = login
