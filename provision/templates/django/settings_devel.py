# -*- coding: utf-8 -*-
"""
Django development settings for ${PROJECT_NAME} project.
"""
from . import *


# Debug
DEBUG = True

TEMPLATE_DEBUG = DEBUG


# Application definition
INSTALLED_APPS += (
    'debug_toolbar',
)


MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${PROJECT_NAME}',
        'USER': 'vagrant'
    }
}


# Debug toolbar
INTERNAL_IPS = ('10.0.2.2',)
