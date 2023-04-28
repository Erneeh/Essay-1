"""
Django settings for Projektas project.
Generated by 'django-admin startproject' using Django 3.2.18.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from setuptools._distutils.command.config import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)a5t2&#*m08-8w@6uiz+j1xtd^bdiaegh2+aa&+&1@=@(sl00q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'myapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Projektas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Projektas.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# test
# STATIC_URL = 'Users/User/Desktop/EssayProjektas/Essay/Projektas/myapp/static/'
# STATICFILES_DIRS = os.path.join(BASE_DIR, '/static/'),
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# deploy
STATIC_URL = '/static/'
STATIC_ROOT = '/usr/local/lsws/Example/html/Essay/Projektas/public/static'
STATICFILES_DIRS = os.path.join(BASE_DIR, '/static/'),

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ed.essay.lt@gmail.com'
EMAIL_HOST_PASSWORD = 'pavasaris0012'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51MuidGHAaHEFy9pUtHiT2Ne923zDhmc7gEnf0GCdZY0t0I8hgyFKK5evdMne1Bq5rtQssDCOdaa1M1WSqgjBKDmj00TY2IcgUF'
STRIPE_SECRET_KEY = 'sk_test_51MuidGHAaHEFy9pUlXedXyAcuiclHPTD6BhKbYgOQbR2AIz3snajL1w7pyGeFzTwHlYcX69318InEJ6KRV125H1o00PWLKfCZc'
STRIPE_WEBHOOK_SECRET = "whsec_74c64d1c81f5b47f003a35277279cd3d2392a4b434c2317207140fce5d8b6e0c"
OPENAI_KEY = "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"
