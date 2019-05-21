# -*- coding: utf-8 -*-
"""
Django development settings for luke project.
"""
from . import *  # noqa

# Short key for tests speed up
SECRET_KEY = 'secret'

# Debug
DEBUG = False

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


# Application definition
INSTALLED_APPS += (
)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'luke',
        'USER': 'vagrant'
    }
}


# Simple password hasher for tests speed up
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


# Email, dummy backend for tests speed up
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
