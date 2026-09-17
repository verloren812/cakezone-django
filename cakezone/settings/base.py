"""Common settings of the cakezone project.

Everything that differs between the environments (the secret key, the debug mode,
the allowed hosts) is read from environment variables. The values can be put
into a `.env` file in the project root (see `.env.example`); it is never committed.

The environment-specific modules extend this one:
    cakezone.settings.dev   - local development (used by manage.py by default)
    cakezone.settings.prod  - production (used by wsgi.py / asgi.py by default)
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# cakezone/settings/base.py -> the project root is three levels up
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# variables that are already set in the environment take precedence over .env
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    """Read a boolean flag: 1/true/yes/on mean True."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    """Read a comma separated list, ignoring blanks."""
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


# the values below are overridden in dev.py / prod.py
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = False
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # applications of the site sections
    "main",
    "menu",
    "team",
    "service",
    "contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cakezone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],      # the base template lives here
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # shared data for the header and the footer: establishment, contacts, categories
                "main.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "cakezone.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]       # css, images, lib from the template
STATIC_ROOT = BASE_DIR / "staticfiles"         # target of `manage.py collectstatic`

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"                # uploaded images of the models

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
