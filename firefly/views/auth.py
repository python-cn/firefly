# coding=utf-8
from __future__ import absolute_import
from flask.blueprints import Blueprint
from flask_security import login_required

from firefly.libs.template import render_template

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/')
@login_required
def profile():
    return render_template('security/accounts/profile.html')
