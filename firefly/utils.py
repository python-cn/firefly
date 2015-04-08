# coding=utf-8
from functools import wraps

from werkzeug.utils import secure_filename
from flask import g, request, redirect, url_for
from flask.ext.mako import render_template


def login_required(f):
    @wraps(f)
    def deco(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return deco


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
