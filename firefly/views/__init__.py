from flask import g, request
from firefly import app, babel, config


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(config.LANGUAGES.keys())


@app.before_request
def before_request():
    g.locale = get_locale()
