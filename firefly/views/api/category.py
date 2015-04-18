# coding=utf-8
from flask import jsonify
from flask.views import MethodView

from firefly.models.topic import Category


class CategoryView(MethodView):

    def get(self, name):
        if name is None:
            categories = [
                c.to_json(only=['id', 'name', 'description'])
                for c in Category.objects
            ]
            rs = {'categories': categories, 'status': 200}
        else:
            category = Category.objects(name=name).first()
            if category is None:
                rs = {'status': 404, 'detail': 'not found'}
            else:
                rs = {
                    'status': 200,
                    'category':
                        category.to_json(only=['id', 'name', 'description'])
                }
        return jsonify(rs)

category_view = CategoryView.as_view('category_api')
