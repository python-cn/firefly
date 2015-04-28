# -*- coding: utf-8 -*-

import pytest

from firefly.app import create_app
from firefly.ext import db


@pytest.fixture
def app(request):
    app = create_app('tests/settings.py')
    db_name = app.config['MONGODB_SETTINGS']['db']

    def cleanup():
        db.connection.drop_database(db_name)
    request.addfinalizer(cleanup)
    return app
