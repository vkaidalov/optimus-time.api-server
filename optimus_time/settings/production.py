import django_heroku

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = '*'

CORS_ORIGIN_ALLOW_ALL = True


# This isn't really needed because Heroku creates its own DATABASE_URL setting.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'optimus_time',
        'USER': 'optimus_time_admin',
        'PASSWORD': 'optimus_time',
        'HOST': 'localhost',
        'PORT': ''
    }
}

django_heroku.settings(
    locals(),
    test_runner=False  # to disable black magic interrupting Travis CI builds
)
