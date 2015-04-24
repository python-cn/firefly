# coding=utf-8
from flask.views import MethodView

from flask_security import login_required
from flask_login import current_user

from firefly import login_manager
from firefly.models.user import User


@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()


class FollowView(MethodView):

    decorators = [login_required]

    def get(self, id):
        user = User.objects.get_or_404(id=id)
        if user not in current_user.following:
            current_user.update_one(push_follwing=user)
            user.update_one(push_follwer=current_user)
            return {'status': 200, 'message': 'ok'}
        else:
            return {'status': 400, 'message': 'error'}


class UnfollowView(MethodView):

    decorators = [login_required]

    def get(self, id):
        user = User.objects.get_or_404(id=id)
        if user in current_user.following:
            current_user.update_one(pull_follwing=user)
            user.update_one(pull_follwer=current_user)
            return {'status': 200, 'message': 'ok'}
        else:
            return {'status': 400, 'message': 'error'}
