# coding=utf-8
from functools import wraps

from werkzeug.utils import secure_filename  # noqa
from flask import request
from flask_mako import render_template


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def _deco(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return _deco
    return decorator
