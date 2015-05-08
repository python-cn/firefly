from __future__ import absolute_import
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
                    name=u'python测试' + str(x), description=u'描述',
                    _slug=u'python-slug' + str(x)
                )
            )
        Category.objects.insert(categories)

    def test_list_api(self):
        rv = self.client.get(url_for('api.categorylistapi'))
        assert len(rv.json['categories']) == Category.objects.count()

    def test_list_api_filter(self):
        url = url_for('api.categorylistapi')

        for name in ['', '     ']:
            rv = self.client.get(url, data={'name': name})
            assert len(rv.json['categories']) == Category.objects.count()

        name = u'测试'
        rv = self.client.get(url, data={'name': name})
        count = Category.objects.filter(name__icontains=name).count()
        assert len(rv.json['categories']) == count

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
