from __future__ import absolute_import
# coding=utf-8
from flask import request, jsonify, redirect, url_for
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template, render_template_def
from flask_login import current_user, logout_user

from firefly.models.topic import Category, Post


bp = Blueprint("home", __name__, url_prefix="/")


class HomeView(MethodView):
    def get(self):
        posts = Post.objects.all()
        return render_template('index.html', posts=posts)


class CreateView(MethodView):
    def post(self):
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category', '')
        if category_id.isdigit():
            category_id = int(category_id)
        category = Category.objects.filter(id=category_id).first()
        post = Post(title=title, content=content, category=category)
        post.save()
        html = render_template_def(
            '/widgets/topic_item.html', 'main', post=post, is_new=True)

        return jsonify(ok=0, html=html)


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated():
            return redirect(url_for('index'))
        return render_template('login.html')


class LogoutView(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('index'))


bp.add_url_rule('/', view_func=HomeView.as_view('index'))
bp.add_url_rule('create', view_func=CreateView.as_view('create'))
bp.add_url_rule('login', view_func=LogoutView.as_view('login'))
bp.add_url_rule('logout', view_func=LogoutView.as_view('logout'))
