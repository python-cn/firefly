# coding: utf-8 -*-

from flask import url_for
import pytest

from firefly.models.topic import Category, Post, Comment


@pytest.mark.usefixtures('client_class')
class TestPost:

    def setup(self):
        c = Category.objects.create(
            name=u'python', description=u'描述', _slug=u'python-slug'
        )
        Post.objects.create(
            title=u'标题test', content=u'内容test', category=c
        )

    def test_create(self):
        category = Category.objects.first()
        url = url_for('home.create')
        form = {
            'title': u'标题',
            'content': u'内容喜喜喜喜喜喜',
            'category': category.id,
        }
        rv = self.client.post(url, data=form)
        assert rv.json['ok'] == 0

        assert Post.objects.count() > 1

    def test_detail(self):
        post = Post.objects.first()
        url = url_for('post.detail', id=post.id)
        rv = self.client.get(url)
        data = rv.get_data().decode('utf8')
        assert post.title in data
        assert post.content in data

    def test_comment(self):
        post = Post.objects.first()
        url = url_for('post.detail', id=post.id)
        form = {
            'content': u'评论测试',
        }
        rv = self.client.post(url, data=form, follow_redirects=False)

        assert rv.status_code == 302
        assert Comment.objects.count() == 1
        post.reload()
        assert len(post.comments) == 1
