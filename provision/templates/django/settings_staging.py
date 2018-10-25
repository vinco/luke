# -*- coding: utf-8 -*-
"""
Django staging settings for ${PROJECT_NAME} project.
"""
import os
import urlparse

from . import *  # noqa


DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
]

# Application definition
INSTALLED_APPS += (
)

MIDDLEWARE_CLASSES += (
)


# Database settings
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

DATABASES = {
    'default': {
        'ENGINE': {
            'postgres': 'django.db.backends.postgresql_psycopg2'
        }[url.scheme],
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port
    }
}

# Static files and uploads
MEDIA_ROOT = os.path.realpath(os.path.join(
    os.environ['DATA_DIR'], 'uploads'))

STATIC_ROOT = os.path.realpath(os.path.join(
    os.environ['DATA_DIR'], 'assets'))

MEDIA_URL = '/uploads/'

STATIC_URL = '/static/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'airbrake': {
            'level': 'ERROR',
            'class': 'airbrake.handlers.AirbrakeHandler',
            'api_key': os.environ['AIRBRAKE_API_KEY'],
            'api_url': 'http://errbit.vincolabs.com/notifier_api/v2/notices',
            'env_name': 'development',
        }
    },
    'loggers': {
        'test': {
            'handlers': ['airbrake'],
            'level': 'ERROR'
        },
        'django.request': {
            'handlers': ['airbrake'],
            'propagate': True,
            'level': 'ERROR'
        },
    }
}
