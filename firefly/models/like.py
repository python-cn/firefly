# coding: utf-8

from __future__ import absolute_import
from datetime import datetime

from firefly.ext import db
from .user import User


class Likes(object):

    def __init__(self):
        self.product_id = None
        self.product_type = None

    def __get__(self, instance, owner):
        self.product_id = str(instance.id)
        self.product_type = owner.__name__
        return self

    def __len__(self):
        return Like.objects(
            product_id=self.product_id,
            product_type=self.product_type
        ).count()

    def __getitem__(self, position):
        return Like.objects(
            product_id=self.product_id,
            product_type=self.product_type,
        )[position]

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
            Like.objects.filter(
                product_id=self.product_id,
                product_type=self.product_type,
                user=user
            ).delete()


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
