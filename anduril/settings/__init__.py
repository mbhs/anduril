"""Django settings for Anduril.

Generated by `django-admin startproject` using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from . import secret


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Secret key moved to file
SECRET_PATH = os.path.join(BASE_DIR, "anduril", "settings", "secret.txt")
SECRET_KEY = secret.get(SECRET_PATH)

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost"]


# Application definition

INSTALLED_APPS = [
    "core",
    "api",
    "home",
    "mail",
    "groups",
    "polymorphic",
    "corsheaders",
    "oauth2_provider",
    "oidc_provider",
    "rest_framework",
    "crispy_forms",
    "sass_processor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "anduril.staticfiles.CustomStaticFilesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "oidc_provider.middleware.SessionManagementMiddleware",
]

ROOT_URLCONF = "anduril.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # Comment to use template cache
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            # "loaders": [
            #     ("django.template.loaders.cached.Loader", [
            #       "django.template.loaders.filesystem.Loader",
            #       "django.template.loaders.app_directories.Loader"]),
            # ]
        },
    },
]

WSGI_APPLICATION = "anduril.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "USER": "",
        "PASSWORD": "",
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# https://github.com/jrief/django-sass-processor

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

SASS_PROCESSOR_ROOT = STATIC_ROOT

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]


# Login URL
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-LOGIN_URL

LOGIN_URL = "home:login"


# CORS setup
# https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_01.html

CORS_ORIGIN_ALLOW_ALL = True


# Django REST framework and OAuth2
# http://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    )
}

OAUTH2_PROVIDER = {
    "SCOPES": {"read": "Read scope", "write": "Write scope"}
}


# OIDC Provider
# http://django-oidc-provider.readthedocs.io/en/v0.5.x/sections/scopesclaims.html

SITE_URL = "http://localhost:8000/"

# OIDC_USERINFO = "anduril.settings.oidc.user_info"

OIDC_EXTRA_SCOPE_CLAIMS = "anduril.settings.oidc.CustomScopeClaims"
OIDC_SESSION_MANAGEMENT_ENABLE = True
