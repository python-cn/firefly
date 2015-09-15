# coding: utf-8

from __future__ import absolute_import

from flask_restful import Resource
from flask_security import login_required
from flask_login import current_user

from firefly.models.topic import Post


class LikePostApi(Resource):

    method_decorators = [login_required]

    def put(self, id):
        post = Post.objects.get_or_404(id=id)
        if post:
            post.likes.add(current_user.id)
        return '', 201

    def delete(self, id):
        post = Post.objects.get_or_404(id=id)
        if post:
            post.likes.delete(current_user.id)
        return '', 201
