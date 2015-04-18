# coding=utf-8
from flask.blueprints import Blueprint

from .category import category_view

bp = Blueprint("api", __name__, url_prefix="/api")

bp.add_url_rule('/category/', defaults={'name': None}, view_func=category_view)
bp.add_url_rule('/category/<string:name>', view_func=category_view)
