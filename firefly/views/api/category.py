# coding=utf-8
from collections import OrderedDict

from flask_restful import Resource, fields, marshal, reqparse

from firefly.models.topic import Category
from .consts import OK, NOTFOUND
from .utils import generate_status_fields


category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


class CategoryListApi(Resource):
    def get(self):
        args = parser.parse_args()
        name = args['name']
        if name is None:
            categories = Category.objects
        else:
            categories = Category.objects.filter(name__icontains=name)
        categories = list(categories)

        status_fields = generate_status_fields(OK)
        return OrderedDict(
            {'categories': marshal(categories, category_fields)},
            **status_fields
        )


class CategoryApi(Resource):
    def get(self, slug):
        category = Category.objects(_slug=slug).first()
        if category is None:
            status_fields = generate_status_fields(NOTFOUND)
            return status_fields
        else:
            status_fields = generate_status_fields(OK)
            return OrderedDict(marshal(category, category_fields),
                               **status_fields)
