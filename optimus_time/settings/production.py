import django_heroku

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = '*'

CORS_ORIGIN_ALLOW_ALL = True

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': ''
    }
}

django_heroku.settings(
    locals(),
    test_runner=False  # to disable black magic interrupting Travis CI builds
)
