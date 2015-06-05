# coding: utf-8 -*-
from __future__ import absolute_import

from flask import url_for
import pytest

from firefly.models.topic import Category, Post, Comment


@pytest.mark.usefixtures('client_class')
class TestPost:

    def setup(self):
        c = Category.objects.create(
            name='python', description='描述', _slug='python-slug'
        )
        Post.objects.create(
            title='标题test', content='内容test', category=c
        )
        self._login()

    def test_create(self):

        category = Category.objects.first()
        url = url_for('home.create_topic')
        form = {
            'title': '标题',
            'content': '内容喜喜喜喜喜喜',
            'category': category.id,
        }
        rv = self.client.post(url, data=form)

        assert rv.json['ok'] == 0
        assert Post.objects.count() > 1

    def test_detail(self):
        post = Post.objects.first()
        url = url_for('post.detail', id=post.id)
        rv = self.client.get(url)
        data = rv.get_data().decode('utf-8')
        assert post.title in data
        assert post.content in data

    def test_comment(self):
        post = Post.objects.first()
        url = url_for('home.create_comment')
        form = {
            'content': '评论测试',
            'ref_id': post.id,
        }
        self.client.post(url, data=form, follow_redirects=False)
        post.reload()

        assert Comment.objects.count() == 1
        assert len(post.comments) == 1
