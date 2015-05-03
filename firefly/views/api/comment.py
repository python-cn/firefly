# coding=utf-8
from __future__ import absolute_import

from flask_restful import Resource

from firefly.models.topic import Comment
from firefly.views.utils import short_timesince
from firefly.views.api.consts import OK
from firefly.views.api.utils import generate_status_fields


class ReplyApi(Resource):
    def get(self, id):
        comment = Comment.objects.get_or_404(id=id)
        replies = comment.get_replies()
        status_fields = generate_status_fields(OK)
        res = []
        for reply in replies:
            author = reply.author
            res.append({
                'id': reply.id,
                'author_name': author.name,
                'author_avatar': author.avatar,
                'author_url': author.url,
                'author_title': '',
                'content': reply.content,
                'short_create_at': short_timesince(reply.created_at),
                'short_create_at': reply.created_at
            })
        status_fields.update({'result': res})
        return status_fields
