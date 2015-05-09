# coding=utf-8
from __future__ import absolute_import

from flask.views import MethodView
from flask.blueprints import Blueprint


bp = Blueprint('user', __name__, url_prefix='/user')


class UserView(MethodView):
    def get(self, id):
        return ''

bp.add_url_rule('/<id>/', view_func=UserView.as_view('detail'))
