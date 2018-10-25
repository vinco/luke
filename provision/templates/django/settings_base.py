# -*- coding: utf-8 -*-
"""
Django settings for ${PROJECT_NAME} project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*+a9uub1)_lc7)fxhba4$%g2#&shao3o))4=_t&k7dyrr3)l47'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
)

# Third party apps.
THIRD_PARTY_APPS = (
    'drf_yasg',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = '${PROJECT_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.realpath(os.path.join(BASE_DIR, '..', 'templates'))
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = '${PROJECT_NAME}.wsgi.application'

# DJango-rest-framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PAGINATION_CLASS': (
        '${PROJECT_NAME}.utils.pagination.ProjectDefaultPagination'
    )
}


# JWT_AUTH for jwt
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': (
        'rest_framework_jwt.utils.jwt_encode_handler'
    ),
    'JWT_DECODE_HANDLER': (
        'rest_framework_jwt.utils.jwt_decode_handler'
    ),
    'JWT_PAYLOAD_HANDLER': (
        'rest_framework_jwt.utils.jwt_payload_handler'
    ),
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': (
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler'
    ),
    'JWT_RESPONSE_PAYLOAD_HANDLER': (
        'rest_framework_jwt.utils.jwt_response_payload_handler'
    ),
    'VJWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1800),
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
 AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PRODUCTION = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.realpath(os.path.join(BASE_DIR, '..', 'assets')),
)

STATIC_ROOT = os.path.realpath(
    os.path.join(BASE_DIR, '..', '..', 'media', 'assets')
)

# User uploaded files

MEDIA_ROOT = os.path.realpath(
    os.path.join(BASE_DIR, '..', '..', 'media', 'uploads')
)

MEDIA_URL = '/media/uploads/'

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
DEFAULT_FROM_EMAIL = "Desarrollo <python@vincoorbis.com>"
EMAIL_FILE_PATH = os.path.realpath(os.path.join(
    BASE_DIR, '..', '..', 'media', 'email'
))
