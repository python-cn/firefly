# coding=utf-8
from flask import jsonify
from flask.views import MethodView
from flask.blueprints import Blueprint

from firefly.models import Category


bp = Blueprint("api", __name__, url_prefix="/api")


class CategoryView(MethodView):

    def get(self, name):
        if name is None:
            categories = [
                {'id': c.id, 'name': c.name, 'description': c.description}
                for c in Category.objects
            ]
            return jsonify({'categories': categories})
        else:
            category = Category.objects(name=name)
            if category is None:
                return jsonify({'status': '204', 'detail': 'not found'})
            else:
                c = {'id': category.id, 'name': category.name,
                     'description': category.description}
                return jsonify(c)

category_view = CategoryView.as_view('category_api')
bp.add_url_rule('/category/', defaults={'name': None}, view_func=category_view)
bp.add_url_rule('/category/<string:name>', view_func=category_view)
