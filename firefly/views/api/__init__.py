# coding=utf-8
from firefly import api

from .category import CategoryApi, CategoryListApi


api.add_resource(CategoryListApi, '/categories')
api.add_resource(CategoryApi, '/category/<name>')
