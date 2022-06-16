"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3^tn^3x$=(dx(whzib2t_y^0()c*bv6i_!7ft*w4_-4n#7rs$v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ORIGIN_ALLOW_ALL = True

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
    # custom apps
    "accounts",
    "datahub",
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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

PROFILE_PICTURES_ROOT = os.path.join(MEDIA_URL, "users")
PROFILE_PICTURES_URL = "users/profile_pictures/"

ORGANIZATION_IMAGES_ROOT = os.path.join(MEDIA_URL, "organizations")
ORGANIZATION_IMAGES_URL = "organizations/logos/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Email configuration
# SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "send_grid_key")
# SENDGRID_API_KEY = os.environ.get("EMAIL_HOST_USER", "email_host_user")
SENDGRID_API_KEY = "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"
EMAIL_HOST_USER = "farmstack.dg@gmail.com"
# User OTP config
OTP_DURATION = 120
OTP_LIMIT = 3

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
            "level": "WARNING",
        },
    },
}

# Enabl CORS headers
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'https://127.0.0.1:8000'
# )

INTERNAL_IPS = ["127.0.0.1", "fe3a-106-51-85-143.ngrok.io"]
