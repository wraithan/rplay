"""Common settings and globals."""
from os.path import abspath, basename, dirname, join, normpath


DJANGO_ROOT = dirname(dirname(abspath(__file__)))
PROJ_ROOT = join(DJANGO_ROOT, "replayswithfriends")
SITE_ROOT = dirname(DJANGO_ROOT)

SITE_NAME = basename(DJANGO_ROOT)

DEBUG = False
PROD = False
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Issac Kelly', 'issac.kelly@gmail.com'),
)
MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'replayswithfriends',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True


MEDIA_ROOT = normpath(join(PROJ_ROOT, 'packaged', 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = normpath(join(PROJ_ROOT, 'packaged', 'static'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_PARSER = 'compressor.parser.LxmlParser'
COMPRESS_PRECOMPILERS = [
    ('text/less', 'lessc {infile} {outfile}'),
]

STATICFILES_DIRS = [
    normpath(join(DJANGO_ROOT, 'static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


SECRET_KEY = r"g_$uq_mh0bi*ahfom_*j(0^%$0p)nj6hk80a@g!@z6xtujb@hl"


FIXTURE_DIRS = [
    normpath(join(DJANGO_ROOT, 'fixtures')),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
]


TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]


TEMPLATE_DIRS = [
    normpath(join(DJANGO_ROOT, 'templates')),
]



MIDDLEWARE_CLASSES = [
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = '%s.urls' % SITE_NAME


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'compressor',
    'djcelery',
    'friendship',
    'gunicorn',
    'queued_storage',
    'south',
    'pagination',

    'replayswithfriends.profiles',
    'replayswithfriends.sc2match',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
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


from datetime import timedelta
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)
from djcelery import setup_loader
setup_loader()

LOGIN_URL = '/players/login/'
LOGIN_REDIRECT_URL = "/sc2/match/"


WSGI_APPLICATION = 'replayswithfriends.wsgi.application'
