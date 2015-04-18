# coding=utf-8
from flask.blueprints import Blueprint
from flask_mako import render_template
from flask_security import login_required

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/')
@login_required
def profile():
    return render_template('accounts/profile.html')
