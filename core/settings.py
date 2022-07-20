"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import collections
import os
from datetime import timedelta
from pathlib import Path

collections.Callable = collections.abc.Callable


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3^tn^3x$=(dx(whzib2t_y^0()c*bv6i_!7ft*w4_-4n#7rs$v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Test cases configuration
# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Tell nose to measure coverage on the datahub, accounts, core and participants apps
NOSE_ARGS = [
    "--cover-html",
    "--cover-package=datahub,accounts,core, participants",
]
# Application definition

INSTALLED_APPS = [
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "debug_toolbar",
    "drf_yasg",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_nose",
    "django_filters",
    "drf_generators",
    # custom apps
    "accounts",
    "datahub",
    "participant",
]
# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=datahub,participant",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
        "OPTIONS": {
            "client_encoding": "UTF8",
        },
    }
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media/"),
]

if not os.path.exists(STATIC_URL):
    os.makedirs(STATIC_URL)  # create the content directory

DOCUMENTS_ROOT = os.path.join(BASE_DIR, "media/documents/")
DOCUMENTS_URL = "media/documents/"
if not os.path.exists(DOCUMENTS_ROOT):
    os.makedirs(DOCUMENTS_ROOT)  # create the temp directory

THEME_ROOT = os.path.join(BASE_DIR, "media/theme/")
THEME_URL = "media/theme/"
# if not os.path.exists(THEME_ROOT):
#     os.makedirs(THEME_ROOT)  # create the temp directory

PROFILE_PICTURES_ROOT = os.path.join(MEDIA_URL, "users")
PROFILE_PICTURES_URL = "users/profile_pictures/"
ORGANIZATION_IMAGES_URL = "organizations/logos/"
ISSUE_ATTACHEMENT_URL = "users/tickets/"
SOLUCTION_ATTACHEMENT_URL = "users/tickets/soluctions/"
SAMPLE_DATASETS_URL = "users/datasets/sample_data/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

# Email configuration
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "send_grid_key")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "email_host_user")

USE_X_FORWARDED_HOST = True

# User OTP config
OTP_DURATION = 900
OTP_LIMIT = 3
USER_SUSPENSION_DURATION = 300

# Store cache in file
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        # 'LOCATION': '/var/django_cache/'
        "LOCATION": os.path.join(BASE_DIR, "django_cache/"),
    }
}

# Fixtures
FIXTURE_DIRS = [
    "fixtures",
]

# drf-spectacular - API documentation settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Datahub API",
    "DESCRIPTION": "API for datahub",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # OTHER SETTINGS
}

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        # information regarding filters
    },
    "formatters": {
        "Simple_Format": {
            "format": "{levelname} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/log_file.log",
            "formatter": "Simple_Format",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
    },
}

# Enable CORS headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'https://127.0.0.1:8000'
# )

INTERNAL_IPS = [
    "127.0.0.1",
]

# FILE HANDLING
FILE_UPLOAD_MAX_SIZE = 2
FILE_TYPES_ALLOWED = ["pdf", "doc", "docx"]
IMAGE_TYPES_ALLOWED = ["jpg", "jpeg", "png"]
TEMP_FILE_PATH = "/tmp/datahub/"
CSS_FILE_NAME = "override.css"

CSS_ROOT = os.path.join(BASE_DIR, "media/theme/css/")
CSS_URL = "media/theme/css/"

if not os.path.exists(CSS_ROOT):
    os.makedirs(CSS_ROOT)  # create the temp directory

if not os.path.exists(TEMP_FILE_PATH):
    os.makedirs(TEMP_FILE_PATH)  # create the temp directory

if not os.path.exists("logs"):
    os.makedirs("logs")  # create the logs directory
