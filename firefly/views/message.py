# coding=utf-8
from __future__ import absolute_import

from flask import request, redirect, url_for
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template
from flask_login import current_user, login_required
from flask_mongoengine.wtf import model_form
from mongoengine.queryset import Q

from firefly.models.message import Message
from firefly.models.user import User


bp = Blueprint("message", __name__, url_prefix="/message")


class IndexView(MethodView):
    decorators = [login_required]

    def get(self):
        author_id = current_user.id
        messages = Message.objects.filter(
            Q(receiver=author_id) | Q(sender=author_id)
        ).order_by("-created_at")

        return render_template('messages/list.html',
                               current_user=current_user,
                               messages=messages)


class DetailView(MethodView):
    decorators = [login_required]

    form = model_form(Message, only=['content'])

    def get(self, id):
        author_id = current_user.id
        user = User.objects.get_or_404(id=id)

        messages = Message.objects.filter(
            (Q(receiver=id) & Q(sender=author_id)) |
            (Q(receiver=author_id) & Q(sender=id))
        ).order_by("-created_at")

        return render_template('messages/detail.html',
                               user=user,
                               form=self.form(request.form),
                               messages=messages)

    def post(self, id):
        form = self.form(request.form)

        if form.validate_on_submit():
            message = Message()
            message.sender = User.objects.get(id=current_user.id)
            message.receiver = User.objects.get(id=id)
            message.content = form.content.data
            message.save()

        return redirect(url_for('message.detail', id=id))


bp.add_url_rule('/', view_func=IndexView.as_view('index'))
bp.add_url_rule('/<id>/', view_func=DetailView.as_view('detail'))
