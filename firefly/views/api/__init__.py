from __future__ import absolute_import
# coding=utf-8
from flask import Blueprint
from flask_restful import Api

from .category import CategoryApi, CategoryListApi
from .comment import ReplyApi
from .user import FollowUserApi, BlockUserApi

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)
api.add_resource(CategoryListApi, '/categories')
api.add_resource(CategoryApi, '/categories/<slug>')
api.add_resource(FollowUserApi, '/users/<id>/follow')
api.add_resource(BlockUserApi, '/users/<id>/block')
api.add_resource(ReplyApi, 'posts/<int:id>/replies')
