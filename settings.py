"""
Django settings for polls project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

DOMAIN = 'polls.subjoin.net'

import socket
PRODUCTION = socket.getfqdn(socket.gethostname()).endswith('dreamhost.com')

import json
import sys
secret_file = os.path.expanduser('~/.django_secrets.json')

if not os.path.isfile(secret_file):
    old_umask = os.umask(0077)
    try:
        with open(secret_file, 'w') as secrets:
            import string
            from random import choice
            secret_key = ''.join([choice(
                    string.letters + string.digits + string.punctuation)
                    for i in range(50)])
            json.dump({'SECRET_KEY': secret_key}, secrets, indent=2)
            secrets.write('\n')
    finally:
        os.umask(old_umask)

with open(secret_file) as secrets:
    stuff = json.load(secrets)
    for k, v in stuff.items():
        # json returns unicode objects, but module definitions are strs.
        setattr(sys.modules[__name__], k.encode('UTF-8'), v.encode('UTF-8'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not PRODUCTION

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'polls',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',

            'OPTIONS': {
                'read_default_file': os.path.expanduser('~/.my.cnf'),
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

if PRODUCTION:
    STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
