# coding: utf-8

from __future__ import absolute_import
from datetime import datetime

from firefly.ext import db
from .user import User


class Likes(object):
    def __init__(self, product_type):
        self.product_type = product_type
        self._instance = None

    def __get__(self, instance, owner):
        self._instance = instance
        return self

    def __len__(self):
        return Like.objects(
            product_id=self.product_id,
            product_type=self.product_type
        ).count()

    def productidgetter(self, func):
        return func

    @property
    def product_id(self):
        return str(self.productidgetter(self._instance))

    def add(self, user_id):
        user = User.objects(id=user_id).first()
        if user:
            return Like.objects.create(
                product_id=self.product_id,
                product_type=self.product_type,
                user=user
            )

    def delete(self, user_id):
        user = User.objects(id=user_id).first()
        if user:
            like = Like.objects.filter(
                product_id=self.product_id,
                product_type=self.product_type,
                user=user
            ).first()
            if like:
                like.delete()


class Like(db.Document):
    id = db.SequenceField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.utcnow, required=True)
    product_type = db.StringField(required=True)
    product_id = db.StringField(required=True,
                                unique_with=['user', 'product_type'])
    user = db.ReferenceField(User)

    meta = {
        'indexes': ['product_type', 'product_id']
    }
