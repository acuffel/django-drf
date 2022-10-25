"""
MyApp base settings.
"""

import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from utils.secret_key import generate_secret_key

from .allauth import *  # noqa: F401,F403
from .auth import *  # noqa: F401,F403
from .celery import *  # noqa: F401,F403
from .drf import *  # noqa: F401,F403
from .logging import *  # noqa: F401,F403

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
APPS_DIR = BASE_DIR / "apps"
sys.path.append(str(APPS_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get("SECRET_KEY", generate_secret_key()))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get("DEBUG", "False")) == "True"
MESSAGE_LEVEL = 10  # DEBUG

# Allowed hosts
# ALLOWED_HOSTS = str(os.environ.get("ALLOWED_HOSTS", "localhost")).split(" ")
ALLOWED_HOSTS = ["127.0.0.1", "host.docker.internal", "localhost", "[::1]"]

# CSRF
# New in Django 4.0: https://docs.djangoproject.com/en/4.0/releases/4.0/#csrf
CSRF_TRUSTED_ORIGINS = ["https://" + ALLOWED_HOSTS[0]]

# Application definition
INSTALLED_APPS = [
    # before "accounts" to override SiteAdmin  # `allauth` needs this from django:
    "django.contrib.sites",
    # before "django.contrib.auth" to override templates:
    "accounts.apps.AccountsConfig",
    "modeltranslation",  # before "django.contrib.admin" to use the admin integration
    "django.contrib.admin",
    "django.contrib.auth",  # `allauth` needs this from django
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",  # `allauth` needs this from django
    "django.contrib.staticfiles",
    "django.contrib.postgres",  # to use HStoreField
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.gitlab",
    "django_celery_results",
    "rest_framework",
    "django_filters",
    "widget_tweaks",
    "debug_toolbar",
    "corsheaders",
    # Core apps
    "core.apps.CoreConfig",
]

# Middewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # after "SessionMiddleware" and "CacheMiddleware" ; before "CommonMiddleware":
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

# Specify site ID because we are using django.contrib.sites
SITE_ID = 1

# Root urls
ROOT_URLCONF = "myapp.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                # `allauth` needs this from django:
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.menu",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "myapp.wsgi.application"

# Database
POSTGRES_HOST = str(os.environ.get("POSTGRES_HOST", ""))
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_DB = str(os.environ.get("POSTGRES_DB", ""))
POSTGRES_USER = str(os.environ.get("POSTGRES_USER", POSTGRES_DB))
POSTGRES_PASSWORD = str(os.environ.get("POSTGRES_PASSWORD", POSTGRES_USER))

if POSTGRES_HOST and POSTGRES_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Cache
REDIS_HOST: str = str(os.environ.get("REDIS_HOST", ""))
REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB: int = int(os.environ.get("REDIS_DB", "0"))

# i18n
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ("fr", _("French")),
    ("en", _("English")),
)
MODELTRANSLATION_FALLBACK_LANGUAGES = ("fr",)

# Time zone
TIME_ZONE = "UTC"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email
EMAIL_HOST = str(os.environ.get("EMAIL_HOST", "smtp.example.com"))
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = str(os.environ.get("EMAIL_HOST_USER", "webmaster@example.com"))
EMAIL_HOST_PASSWORD = str(os.environ.get("EMAIL_HOST_PASSWORD", "password"))
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS", "True")) == "True"
EMAIL_USE_SSL = str(os.environ.get("EMAIL_USE_SSL", "False")) == "True"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if DEBUG or EMAIL_HOST == "smtp.example.com":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Core App
CORE_DEFAULT_SITE_NAME = str(os.environ.get("APP_SITE_NAME", "No Site Name!"))
CORE_SITECUSTOMIZATION_TAGLINE_LENGHT = 255
CORE_SITECUSTOMIZATION_DESCRIPTION_LENGHT = 2048

# Django Debug Toolbar
def show_toolbar(request):  # noqa E302
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

# Default Charfield Maxlenght
MY_APP_CHAR_MAX_LENGTH = 255

# CORS Django REST Framework
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ( 
#   'http://localhost:8000',
# )
