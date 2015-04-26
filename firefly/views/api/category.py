# coding=utf-8
from collections import OrderedDict

from flask_restful import Resource, fields, marshal

from firefly.models.topic import Category
from .utils import generate_status_fields


category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}


class CategoryListApi(Resource):
    def get(self):
        categories = [
            c for c in Category.objects
        ]
        status_fields = generate_status_fields(200, 'ok')
        return OrderedDict(
            {'categories': marshal(categories, category_fields)},
            **status_fields
        )


class CategoryApi(Resource):
    def get(self, slug):
        category = Category.objects(_slug=slug).first()
        if category is None:
            status_fields = generate_status_fields(404, 'not_found')
            return status_fields
        else:
            status_fields = generate_status_fields(200, 'ok')
            return OrderedDict(marshal(category, category_fields),
                               **status_fields)
