from __future__ import absolute_import
# coding=utf-8
from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource

from firefly.models.user import User
from .consts import OK, NOTFOUND, EXISTING
from .utils import generate_status_fields


class FollowUserApi(Resource):

    method_decorators = [login_required]

    def put(self, id):
        user = User.objects(id=id).first()
        if user is None:
            status_fields = generate_status_fields(NOTFOUND)
            return status_fields, 404
        if user not in current_user.following:
            current_user.update_one(push_follwing=user)
            user.update_one(push_follwer=current_user)
            status_fields = generate_status_fields(OK)
        else:
            status_fields = generate_status_fields(EXISTING)
        return status_fields, 202

    def delete(self, id):
        user = User.objects(id=id).first()
        if user is None:
            status_fields = generate_status_fields(NOTFOUND)
            return status_fields, 404
        if user in current_user.following:
            current_user.update_one(pull_follwing=user)
            user.update_one(pull_follwer=current_user)
            status_fields = generate_status_fields(OK)
        else:
            status_fields = generate_status_fields(NOTFOUND)
        return status_fields, 204


class BlockUserApi(Resource):

    method_decorators = [login_required]

    def put(self, id):
        user = User.objects(id=id).first()
        if user is None:
            status_fields = generate_status_fields(NOTFOUND)
            return status_fields, 404
        if id not in current_user.blocked_user_id:
            current_user.update_one(push_blocked_user_id=id)
            status_fields = generate_status_fields(OK)
        else:
            status_fields = generate_status_fields(EXISTING)
        return status_fields, 202

    def delete(self, id):
        user = User.objects(id=id).first()
        if user is None:
            status_fields = generate_status_fields(NOTFOUND)
            return status_fields, 404
        if id in current_user.blocked_user_id:
            current_user.update_one(pull_blocked_used_id=id)
            status_fields = generate_status_fields(OK)
        else:
            status_fields = generate_status_fields(NOTFOUND)
        return status_fields, 204
