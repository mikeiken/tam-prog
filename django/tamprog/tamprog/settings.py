"""
Django settings for tamprog project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_IN_CONTAINER = bool(os.getenv('IS_IN_CONTAINER', 'false').lower() == 'true')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-sihuf!9sq3^(+b2=z5taf$^6mszw^$e=1k%-dzj_*#bt3p9*(6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = (os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(','))


# Application definition
AUTH_USER_MODEL = 'user.Person'
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'user',
    'garden',
    'orders',
    'plants',
    'fertilizer',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tamprog.urls'

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

WSGI_APPLICATION = 'tamprog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'garden'),
        'HOST': os.getenv('DJANGO_DB_HOST', '127.0.0.1') \
            if IS_IN_CONTAINER \
            else '127.0.0.1',
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'root'),
        'USER': os.getenv('POSTGRES_USER', 'agronom'),
    },
    # 'test': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static-dj/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-dj')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
    "http://homelab.kerasi.ru",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
    'UPDATE',
    'DESTROY'
]

# Content Security Policy (CSP)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-eval'",
    "https://mc.yandex.ru",
)
CSP_FRAME_SRC = (
    "'self'",
    "https://example.com",
)

CSP_CONNECT_SRC = (
    "'self'",
    'https://example.com',
    "https://mc.yandex.ru",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://homelab.kerasi.ru",
)

CSRF_TRUSTED_ORIGINS = [
    'https://example.com',
    "http://localhost:3000",
    "http://localhost:8000",
    "http://homelab.kerasi.ru",
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Tamprog API',
    'DESCRIPTION': 'API documentation for Tamprog',
    'VERSION': '1.0.0',
    "SERVE_INCLUDE_SCHEMA": True, # исключить эндпоинт /schema
    "SWAGGER_UI_SETTINGS": {
        "filter": True, # включить поиск по тегам
    },
    "COMPONENT_SPLIT_REQUEST": True,
}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    #'PAGE_SIZE': 30
}

SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

DJANGO_ASYNC_TIMEOUT_S = float(os.getenv('DJANGO_ASYNC_TIMEOUT_S', '30'))

RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost') \
    if IS_IN_CONTAINER \
    else 'localhost'
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')

CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

CELERY_BROKER_CONNECTION_RETRY = bool(os.getenv(
    'CELERY_BROKER_CONNECTION_RETRY', 'True').lower() == 'true')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = bool(os.getenv(
    'CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP', 'True').lower() == 'true')
CELERY_BROKER_CONNECTION_MAX_RETRIES = int(os.getenv(
    'CELERY_BROKER_CONNECTION_MAX_RETRIES', '10'))
CELERY_BROKER_HEARTBEAT = int(os.getenv(
    'CELERY_BROKER_HEARTBEAT', '60'))
CELERY_WORKER_PREFETCH_MULTIPLIER = int(os.getenv(
    'CELERY_WORKER_PREFETCH_MULTIPLIER', '1') \
    if IS_IN_CONTAINER \
    else '1')

CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', 'rpc://')
# Acknowledge tasks after they are done [True/False]
CELERY_TASK_ACKS_LATE = bool(os.getenv(
    'CELERY_TASK_ACKS_LATE', 'True').lower() == 'true')
# Run tasks synchronously [True/False]
CELERY_TASK_ALWAYS_EAGER = bool(os.getenv(
    'CELERY_TASK_ALWAYS_EAGER', 'False').lower() == 'true')
# Use a single worker process ['solo', 'prefork']
CELERY_WORKER_POOL = os.getenv(
    'CELERY_WORKER_POOL', 'solo') \
    if IS_IN_CONTAINER \
    else 'solo'
# Restart worker after each task
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(os.getenv(
    'CELERY_WORKER_MAX_TASKS_PER_CHILD', '1') \
    if IS_IN_CONTAINER \
    else '1')
# Number of worker processes
CELERY_WORKER_CONCURRENCY = int(os.getenv(
    'CELERY_WORKER_CONCURRENCY', '1') \
    if IS_IN_CONTAINER \
    else '1')
# Disable result printing
CELERY_TASK_IGNORE_RESULT = bool(os.getenv(
    'CELERY_TASK_IGNORE_RESULT', 'False').lower() == 'true')
# Configure task logging
CELERY_WORKER_REDIRECT_STDOUTS = bool(os.getenv(
    'CELERY_WORKER_REDIRECT_STDOUTS', 'True').lower() == 'true')
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = os.getenv(
    'CELERY_WORKER_REDIRECT_STDOUTS_LEVEL', 'INFO')
# Custom logging format for tasks
CELERY_WORKER_TASK_LOG_FORMAT = (
    os.getenv('CELERY_WORKER_TASK_LOG_FORMAT', '%(asctime)s - %(message)s')
)