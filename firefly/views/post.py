# coding=utf-8
from __future__ import absolute_import
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mongoengine.wtf import model_form

from firefly.models.topic import Post, Comment
from firefly.libs.template import render_template


bp = Blueprint("post", __name__, url_prefix="/post")


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at', 'author', 'id'])

    def get(self, id):
        post = Post.objects.get_or_404(id=id)
        Post.objects(id=id).update_one(inc__views=1)
        return render_template('posts/detail.html', post=post)

bp.add_url_rule('/<int:id>/', view_func=DetailView.as_view('detail'))
