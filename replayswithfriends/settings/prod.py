"""Production settings and globals."""


from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from common import *


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

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'ketama': True,
        }
    }
}


########## CELERY CONFIGURATION
BROKER_TRANSPORT = 'amqplib'
BROKER_URL = env('RABBITMQ_URL', '')
CELERY_RESULT_BACKEND = 'amqp'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 5
########## END CELERY CONFIGURATION



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
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')

STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = STATIC_URL

SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)