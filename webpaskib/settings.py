"""
Django settings for webpaskib project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
import os
from django.apps import AppConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-uh**1=z&b*an1!$xwqsfql9los8#9st2tvm!x#w$x3(@%m+jgo"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ff7a-36-68-220-207.ngrok-free.app']

CSRF_TRUSTED_ORIGINS =['https://ff7a-36-68-220-207.ngrok-free.app']

CSRF_COOKIE_DOMAIN = 'https://ff7a-36-68-220-207.ngrok-free.app'

SESSION_COOKIE_HTTPONLY = True

CSRF_USE_SESSIONS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    "landing",
    "bayar",
    "user_web",
    "crispy_forms",
    "crispy_bootstrap5",
    'django_cleanup.apps.CleanupConfig',
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'
#Custom user model
AUTH_USER_MODEL = 'user_web.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "webpaskib.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'),
                ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webpaskib.wsgi.application"



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smanstar',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',  # or the hostname where your MySQL server is running
        'PORT': '3306',      # or the port on which your MySQL server is listening
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "id"

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'landing/static'
STATICFILES_DIRS = ['E:\piton\webtikcet\webpaskib\static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MIDTRANS = {
    'MERCHANT_ID': (os.getenv('MIDTRANS_MERCHANT_ID')),
    'SERVER_KEY': os.environ.get('MIDTRANS_SERVER_KEY'),
    'CLIENT_KEY': os.environ.get('MIDTRANS_CLIENT_KEY'),
}

