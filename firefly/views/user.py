# coding=utf-8
from __future__ import absolute_import

from flask import url_for, redirect

from flask.views import MethodView
from flask.blueprints import Blueprint
from flask.ext.login import login_required, current_user
from firefly.libs.template import render_template
from firefly.forms.user import ProfileForm


bp = Blueprint('user', __name__, url_prefix='/user')


class UserView(MethodView):
    def get(self, id):
        return ''


class UserSettingsView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('user/settings.html', user=current_user)

    def post(self):
        form = ProfileForm()
        form.save()
        return redirect(url_for('user.settings'))

bp.add_url_rule('/<id>/', view_func=UserView.as_view('detail'))
bp.add_url_rule('/settings', view_func=UserSettingsView.as_view('settings'))
