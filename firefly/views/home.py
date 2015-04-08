# coding=utf-8
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask.ext.mako import render_template

from firefly.models import Post


bp = Blueprint("home", __name__, url_prefix="/")


class HomeView(MethodView):

    def get(self):
        return render_template('index.html', ctx=self)


class ListView(MethodView):

    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


#bp.add_url_rule('/', view_func=ListView.as_view('list'))
bp.add_url_rule('/', view_func=HomeView.as_view('list'))
