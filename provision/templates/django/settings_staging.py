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
    'opbeat.contrib.django',
)

MIDDLEWARE_CLASSES += (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
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

# Opbeat
OPBEAT = {
    'ORGANIZATION_ID': os.environ['OPBEAT_ORGANIZATION_ID'],
    'APP_ID': os.environ['OPBEAT_APP_ID'],
    'SECRET_TOKEN': os.environ['OPBEAT_SECRET_TOKEN'],
    'INSTRUMENT_DJANGO_MIDDLEWARE': True,
}
