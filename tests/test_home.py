# coding: utf-8 -*-

from flask import url_for
import pytest

from firefly.models.topic import Category, Post


@pytest.mark.usefixtures('client_class')
class TestHome:

    def setup(self):
        c = Category.objects.create(
            name=u'python', description=u'描述', _slug=u'python-slug'
        )
        for x in range(5):
            Post.objects.create(
                title=u'标题test%s' % x, content=u'内容test % x', category=c
            )

    def test_post_list(self):
        posts = Post.objects.all()
        rv = self.client.get(url_for('home.index'))

        data = rv.get_data().decode('utf8')
        for p in posts:
            assert p.title in data

    def test_keyboard(self):
        assert self.client.get(url_for('keyboard.keyboard')).status_code == 200
