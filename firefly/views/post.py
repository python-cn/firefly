# coding=utf-8
from __future__ import absolute_import
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_mongoengine.wtf import model_form

from firefly.models.topic import Post, Comment
from firefly.libs.template import render_template
from firefly.libs.markdown import Markdown
from firefly.views.utils import short_timesince


bp = Blueprint("post", __name__, url_prefix="/post")


def gen_author(p):
    class c(object):
        id = 100001
        name = 'test1'
        avatar = lambda x: 'https://meta-discourse.global.ssl.fastly.net/user_avatar/meta.discourse.org/codinghorror/90/5297.png'  # noqa
        cn = 'Test'

        def url(self):
            return '/user/1000001'
    author = p.author if p.author else c()
    return author


def gen_author_name(p):
    author = gen_author(p)
    return author.username if hasattr(author, 'username') and \
        author.username else author.cn


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at', 'author', 'id'])

    def get(self, id):
        post = Post.objects.get_or_404(id=id)
        Post.objects(id=id).update_one(inc__views=1)
        return render_template('posts/detail.html', post=post, hasattr=hasattr,
                               Markdown=Markdown, gen_author=gen_author,
                               gen_author_name=gen_author_name,
                               short_timesince=short_timesince)

bp.add_url_rule('/<int:id>/', view_func=DetailView.as_view('detail'))
