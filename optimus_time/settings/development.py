from .base import *

SECRET_KEY = '==avaw@p#bpuv2fw3)vel*y93wvqrsfduwm4+g9ri3#i$&_m&l'

DEBUG = True

ALLOWED_HOSTS = '*'

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