# coding: utf-8 -*-

from flask import url_for
import pytest

from firefly.models.topic import Category


@pytest.mark.usefixtures('client_class')
class TestCategory:

    def setup(self):
        categories = []
        for x in range(3):
            categories.append(
                Category(
                    name=u'python' + str(x), description=u'描述',
                    _slug=u'python-slug' + str(x)
                )
            )
        Category.objects.insert(categories)

    def test_list_api(self):
        rv = self.client.get(url_for('api.categorylistapi'))
        assert rv.json['categories']

    def test_detail_api(self):
        category = Category.objects.first()
        url = url_for('api.categoryapi', slug=category.slug)
        rv = self.client.get(url)
        assert rv.json['name'] == category.name

    def test_detail(self):
        category = Category.objects.first()
        rv = self.client.get(url_for('category.detail', slug=category.slug))

        assert rv.status_code == 200
        # TODO test response content
