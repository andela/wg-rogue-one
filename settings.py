#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wger.settings_global import *

# Use 'DEBUG = True' to get more details for server errors
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

ADMINS = (
    ('Your name', 'your_email@example.com'),
)
MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('WG_NAME') or 'test_wger',
        'USER': os.environ.get('WG_USER') or 'postgres',
        'HOST': os.environ.get('WG_HOST') or 'localhost',
        'PASSWORD': os.environ.get('WG_PASSWORD') or '',
        'PORT': os.environ.get('WG_PORT') or '5432',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h*e8yqx#(k3a3nbxnde%7d3fo&@=tz6zv)-blgmtoxch5q0=n&'

# Your reCaptcha keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True

# The site's URL (e.g. http://www.my-local-gym.com or http://localhost:8000)
# This is needed for uploaded files and images (exercise images, etc.) to be
# properly served.
SITE_URL = 'http://localhost:8000'

# Path to uploaded files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = ''
MEDIA_URL = '/media/'

# Allow all hosts to access the application. Change if used in production.
ALLOWED_HOSTS = '*'

# This might be a good idea if you setup memcached
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configure a real backend in production
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sender address used for sent emails
WGER_SETTINGS['EMAIL_FROM'] = 'wger Workout Manager <wger@example.com>'

# Your twitter handle, if you have one for this instance.
#WGER_SETTINGS['TWITTER'] = ''

#Fitbit settings
REDIRECT_URI = os.getenv('REDIRECT_URI', None)
CLIENT_ID = os.getenv('CLIENT_ID',None)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)
SCOPE = ('weight','activity')   # user information wger will have access to
Authorization_URI = os.getenv('Authorization_URI', None)
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', None)

try:
    from local_settings import *
except ImportError:
    pass
