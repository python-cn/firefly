from __future__ import absolute_import
# coding=utf-8
from flask import request
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template

from firefly.models.consts import KEYBOARD_URL_MAPS


bp = Blueprint('keyboard', __name__, url_prefix='/keyboard')


class KeyboardView(MethodView):
    def get(self):
        url = request.args.get('url', '')
        url_pattern = url.rsplit('/', 1)[0]
        keyboards = KEYBOARD_URL_MAPS['default']
        if url_pattern in KEYBOARD_URL_MAPS:
            keyboards += KEYBOARD_URL_MAPS[url_pattern]
        return render_template('widgets/keyboard.html', keyboards=keyboards)


bp.add_url_rule('/', view_func=KeyboardView.as_view('keyboard'))
