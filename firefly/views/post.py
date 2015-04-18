# coding=utf-8
from flask import request, redirect, url_for
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template
from flask_mongoengine.wtf import model_form

from firefly.models.topic import Post, Comment


bp = Blueprint("post", __name__, url_prefix="/post")


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, id):
        post = Post.objects.get_or_404(id=id)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, id):
        context = self.get_context(id)
        return render_template('posts/detail.html', **context)

    def post(self, id):
        context = self.get_context(id)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('post.detail', id=id))
        return render_template('posts/detail.html', **context)

bp.add_url_rule('/<int:id>/', view_func=DetailView.as_view('detail'))
