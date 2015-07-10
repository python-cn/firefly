# coding=utf-8
from flask import render_template as _render_template

from flask_login import current_user
from flask_security.utils import url_for_security


def render_template(template_name_or_list, **context):
    context.update({
        'current_user': current_user,
        'url_for_security': url_for_security
    })
    return _render_template(template_name_or_list, **context)
