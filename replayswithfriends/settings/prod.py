"""Production settings and globals."""


from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from common import *

DEBUG = False

# Helper lambda for gracefully degrading environmental variables:
env = lambda e, d: environ[e] if environ.has_key(e) else d

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', 'your_email@example.com')
EMAIL_PORT = env('EMAIL_PORT', 587)
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = True if env('EMAIL_USE_TLS', 'True') == 'True'  else False
SERVER_EMAIL = EMAIL_HOST_USER



########## DATABASE CONFIGURATION
# See: http://devcenter.heroku.com/articles/django#postgres_database_config
uses_netloc.append('postgres')
uses_netloc.append('mysql')

try:
    if environ.has_key('DATABASE_URL'):
        url = urlparse(environ['DATABASE_URL'])
        DATABASES['default'] = {
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except:
    print "Unexpected error:", exc_info()



########## CELERY CONFIGURATION
BROKER_HOST = 'herring.redistogo.com'
BROKER_PORT = 9920
BROKER_BACKEND = 'redis'
REDIS_HOST = BROKER_HOST
REDIS_PORT = BROKER_PORT
BROKER_VHOST = "0"
BROKER_PASSWORD = 'ec07a0173994aab43a457a6c6c9a761c'
REDIS_PASSWORD = 'ec07a0173994aab43a457a6c6c9a761c'
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS=True
CELERY_TASK_RESULT_EXPIRES =  10
import djcelery
djcelery.setup_loader()


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (REDIS_HOST, REDIS_PORT),
        'OPTIONS': {
            'DB': 0,
            'HOST': REDIS_HOST,
            'PORT': REDIS_PORT,
            'PASSWORD': REDIS_PASSWORD,
            'max_connections': 2,
        },
    },
}

INSTALLED_APPS += [
    'storages',
    'raven.contrib.django',
]

MIDDLEWARE_CLASSES = [
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    ] + MIDDLEWARE_CLASSES + [
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
]

SENTRY_DSN = 'https://783890b5ea754868bbb54dad7632285a:56827db1f54345978e06573aa9755b24@app.getsentry.com/671'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', 'AKIAJ35NWHEJY2Z3VWNQ')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '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')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', 'r-play')


STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = STATIC_URL
CMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False

SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
