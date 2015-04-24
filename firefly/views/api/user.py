# coding=utf-8
from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource

from firefly.models.user import User
from .utils import generate_status_fields


class FollowUserApi(Resource):

    method_decorators = [login_required]

    def put(self, id):
        user = User.objects.get_or_404(id=id)
        if user not in current_user.following:
            current_user.update_one(push_follwing=user)
            user.update_one(push_follwer=current_user)
            status_fields = generate_status_fields(200, 'ok')
        else:
            status_fields = generate_status_fields(404, 'error')
        return status_fields

    def delete(self, id):
        user = User.objects.get_or_404(id=id)
        if user in current_user.following:
            current_user.update_one(pull_follwing=user)
            user.update_one(pull_follwer=current_user)
            status_fields = generate_status_fields(200, 'ok')
        else:
            status_fields = generate_status_fields(404, 'error')
        return status_fields
