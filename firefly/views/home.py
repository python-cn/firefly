# coding=utf-8
from flask import request, jsonify
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask.ext.mako import render_template

from firefly.models.topic import Post


bp = Blueprint("home", __name__, url_prefix="/")


class HomeView(MethodView):
    def get(self):
        posts = Post.objects.all()
        return render_template('index.html', posts=posts)


class CreateView(MethodView):
    def post(self):
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(
            title=title,
            content=content)
        post.save()
        return jsonify(ok=0)


bp.add_url_rule('/', view_func=HomeView.as_view('list'))
bp.add_url_rule('create', view_func=CreateView.as_view('create'))
