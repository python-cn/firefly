# coding=utf-8
from flask.views import MethodView
from flask.blueprints import Blueprint

from flask_security import login_required
from flask_login import current_user

from firefly import login_manager
from firefly.models.user import User


bp = Blueprint("user", __name__, url_prefix="/")


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


class BlockView(MethodView):

    decorators = [login_required]

    def get(self, id):
        user = User.objects.get_or_404(id=id)
        if user in current_user.blocked_user_ids:
            current_user.update_one(push_blocked_user_ids=user.id)
            return {'status': 200, 'message': 'ok'}
        else:
            return {'status': 400, 'message': 'error'}


class UnblockView(MethodView):

    decorators = [login_required]

    def get(self, id):
        user = User.objects.get_or_404(id=id)
        if user in current_user.blocked_user_ids:
            current_user.update_one(pull_blocked_user_ids=user.id)
            return {'status': 200, 'message': 'ok'}
        else:
            return {'status': 400, 'message': 'error'}


bp.add_url_rule('follow/<int:id>',
                view_func=FollowView.as_view('follow'))
bp.add_url_rule('unfollow/<int:id>',
                view_func=UnfollowView.as_view('unfollow'))
bp.add_url_rule('block/<int:id>',
                view_func=BlockView.as_view('block'))
bp.add_url_rule('unblock/<int:id>',
                view_func=UnblockView.as_view('unblock'))
