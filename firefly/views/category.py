from __future__ import absolute_import
# coding=utf-8
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mako import render_template

from firefly.models.topic import Category, Post


bp = Blueprint("category", __name__, url_prefix="/category")


class CategoryView(MethodView):

    def get(self, slug):
        category = Category.objects.get_or_404(_slug=slug)
        posts = Post.objects.filter(
            category=category
        ).order_by("-recent_activity_time")
        return render_template('categories/list.html',
                               category=category.name,
                               posts=posts)

bp.add_url_rule('/<slug>/', view_func=CategoryView.as_view('detail'))
