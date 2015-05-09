# coding=utf-8
from __future__ import absolute_import
from flask import request, jsonify, redirect, url_for
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template, render_template_def
from flask_login import login_user, current_user

from firefly.forms.user import LoginForm, RegisterForm
from firefly.models.topic import Category, Post
from firefly.models.user import User


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
        post = Post(title=title, content=content, category=category,
                    author=User.objects.get_or_404(id=current_user.id))
        post.save()
        html = render_template_def(
            '/widgets/topic_item.html', 'main', post=post, is_new=True)

        return jsonify(ok=0, html=html)


class LoginView(MethodView):
    def get(self):
        return redirect(url_for('home.index'))

    def post(self):
        # TODO 解决在首页登录框中无法获取 csrf_token 的问题
        form = LoginForm(csrf_enabled=False)
        if form.validate_on_submit():
            login_user(form.user)
        return redirect(url_for('home.index'))


class RegisterView(MethodView):
    def get(self):
        return redirect(url_for('home.index'))

    def post(self):
        form = RegisterForm(csrf_enabled=False)
        if form.validate_on_submit():
            user = form.save()
            login_user(user)
        return redirect(url_for('home.index'))


bp.add_url_rule('/', view_func=HomeView.as_view('index'))
bp.add_url_rule('create', view_func=CreateView.as_view('create'))
bp.add_url_rule('login', view_func=LoginView.as_view('login'))
bp.add_url_rule('register', view_func=RegisterView.as_view('register'))
