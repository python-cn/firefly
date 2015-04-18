# coding=utf-8
from flask import jsonify
from flask.views import MethodView

from firefly.models import Category


class CategoryView(MethodView):

    def get(self, name):
        rs = None
        if name is None:
            categories = [
                {'id': c.id, 'name': c.name, 'description': c.description}
                for c in Category.objects
            ]
            rs = {'categories': categories}
        else:
            category = Category.objects(name=name)
            if category is None:
                rs = {'status': '204', 'detail': 'not found'}
            else:
                rs = {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                }
        return jsonify(rs)

category_view = CategoryView.as_view('category_api')
