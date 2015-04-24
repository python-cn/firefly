# coding=utf-8
from flask import Blueprint
from flask_restful import Api

from .category import CategoryApi, CategoryListApi
from .user import FollowUserApi

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)
api.add_resource(CategoryListApi, '/categories')
api.add_resource(CategoryApi, '/categories/<name>')
api.add_resource(FollowUserApi, '/users/<id>/follow')
