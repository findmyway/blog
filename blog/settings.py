#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('BLOG_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# TEMPLATE_DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = False


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles',
    'taggit',
    'django_crontab',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'blog.urls'

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# log

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django_crontab': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# My Settings
CRONJOBS = [
    ('*/2 * * * *', 'django.core.management.call_command', ['yinxiang_articles']),
    ('*/2 * * * *', 'django.core.management.call_command', ['yinxiang_home']),
    ('*/2 * * * *', 'django.core.management.call_command', ['yinxiang_shares']),
    ('*/2 * * * *', 'django.core.management.call_command', ['yinxiang_up_down_load_resources']),
]

# evernote part
NOTEBOOK_ARTICLES = "blog_articles"
NOTEBOOK_HOME = "blog_home"
NOTEBOOK_SHARE = "blog_share"

EVERNOTE_TOKEN = os.getenv('EVERNOTE_TOKEN')

# qiniu part
QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
QINIU_PREFIX = 'blog/resources/'
BUCKET_NAME = 'ontheroad'

# where to store uploaded files
RESOURCES_DIR = '/data/'

# admin
ADMINS = (
    ('TianJun', 'tianjun.cpp@gmail.com'),
)
