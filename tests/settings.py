# coding=utf-8

DEBUG = True
TESTING = True
SECRET_KEY = 'secret_key for test'

# mongodb
MONGODB_SETTINGS = {
    'db': 'firefly_test',
    'username': '',
    'password': '',
    'host': '127.0.0.1',
    'port': 27017
}

# redis cache
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 9
CACHE_REDIS_PASSWORD = ''

# mail sender
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'MAIL_USERNAME'
MAIL_PASSWORD = 'MAIL_PASSWORD'
MAIL_DEFAULT_SENDER = 'admin@python-cn.org'

SECURITY_PASSWORD_SALT = "abc"
SECURITY_PASSWORD_HASH = "bcrypt"
# SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_EMAIL_SENDER = "support@python-cn.org"

SECURITY_CONFIRM_SALT = "570be5f24e690ce5af208244f3e539a93b6e4f05"
SECURITY_REMEMBER_SALT = "de154140385c591ea771dcb3b33f374383e6ea47"

# Set secret keys for CSRF protection
CSRF_ENABLED = False
WTF_CSRF_ENABLED = False

SERVER_EMAIL = 'Python-China <support@python-cn.org>'

# Flask-SocialBlueprint
SOCIAL_BLUEPRINT = {
    # https://developers.facebook.com/apps/
    "flask_social_blueprint.providers.Facebook": {
        # App ID
        'consumer_key': '197…',
        # App Secret
        'consumer_secret': 'c956c1…'
    },
    # https://apps.twitter.com/app/new
    "flask_social_blueprint.providers.Twitter": {
        # Your access token from API Keys tab
        'consumer_key': 'bkp…',
        # access token secret
        'consumer_secret': 'pHUx…'
    },
    # https://console.developers.google.com/project
    "flask_social_blueprint.providers.Google": {
        # Client ID
        'consumer_key': '797….apps.googleusercontent.com',
        # Client secret
        'consumer_secret': 'bDG…'
    },
    # https://github.com/settings/applications/new
    "flask_social_blueprint.providers.Github": {
        # Client ID
        'consumer_key': '6f6…',
        # Client Secret
        'consumer_secret': '1a9…'
    },
}
