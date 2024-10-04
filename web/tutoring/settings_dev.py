"""
Django settings for tutoring project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<secret>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'tutoring.svcover.nl', 'api.telegram.org']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'CoverAccounts',
    'messages',
    'tutors',
    'task',
    'telegram_bot'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'CoverAccounts.middleware.CoverAuthenticationMiddleware',
    'CoverAccounts.middleware.RestrictAdminMiddleware',
    'CoverAccounts.middleware.RestrictUnknownUserMiddleware'
]

ROOT_URLCONF = 'tutoring.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'messages.context_processors.conversationsOfUser',
            ],
        },
    },
]

WSGI_APPLICATION = 'tutoring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'web/development_db',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/app/www/static'

AUTH_USER_MODEL = 'CoverAccounts.CoverMember'
AUTHENTICATION_BACKENDS = ['CoverAccounts.backends.CoversiteAuthBackend', ]

ADMIN_COMMITTEES = ['studcee']
STAFF_MEMBERS = ['rafael@bankosegger.at', 'emily.beuken@gmail.com']

# Cover API settings
# https://bitbucket.org/cover-webcie/coverapi
COVER_API_URL = 'http://coverapi:8001/api.php' # host is coverapi for access from python
COVER_LOGIN_URL = 'http://localhost:8001/api.php?view=login' # host is localhost for access from browser
COVER_LOGOUT_URL = 'http://localhost:8001/api.php?view=logout' # host is localhost for access from browser

COVER_API_APP = 'test-app'
COVER_API_SECRET = 'ultrasecrethashkey'

#Crispy FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_USE_TLS = True


TELEGRAM_BOT_API_TOKEN = '<secret>'
TELEGRAM_HASH_SALT = '<secret>'
