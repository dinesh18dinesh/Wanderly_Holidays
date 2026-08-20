"""
Django settings for travelwebsite project.
Travel and Tourism Website - CDIT_PY_00008
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# Base directory
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only-key"
)

# Development can explicitly set DJANGO_DEBUG=True.
# Production defaults to False.
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

# Local hosts
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

# Render automatically provides the external hostname.
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    if RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",

    # Local apps
    "destinations",
    "bookings",
    "accounts",
    "payments",
]


# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise serves static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ------------------------------------------------------------------------------
# URL configuration
# ------------------------------------------------------------------------------

ROOT_URLCONF = "travelwebsite.urls"


# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# ------------------------------------------------------------------------------
# WSGI / ASGI
# ------------------------------------------------------------------------------

WSGI_APPLICATION = "travelwebsite.wsgi.application"
ASGI_APPLICATION = "travelwebsite.asgi.application"


# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
#
# Local development:
#   Uses SQLite automatically when DATABASE_URL is not present.
#
# Render production:
#   Uses PostgreSQL through the DATABASE_URL environment variable.
#
# ------------------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        )
    },
]


# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ------------------------------------------------------------------------------
# Static files
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise compressed static-file storage
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ------------------------------------------------------------------------------
# Media / user-uploaded files
# ------------------------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ------------------------------------------------------------------------------
# Default primary key
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ------------------------------------------------------------------------------
# Crispy Forms
# ------------------------------------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# ------------------------------------------------------------------------------
# Authentication redirects
# ------------------------------------------------------------------------------

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"


# ------------------------------------------------------------------------------
# Razorpay
# ------------------------------------------------------------------------------

RAZORPAY_KEY_ID = os.environ.get(
    "RAZORPAY_KEY_ID",
    ""
)

RAZORPAY_KEY_SECRET = os.environ.get(
    "RAZORPAY_KEY_SECRET",
    ""
)

# Demo mode automatically enabled when real Razorpay keys are unavailable.
PAYMENTS_DEMO_MODE = not (
    RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
)


# ------------------------------------------------------------------------------
# OpenWeatherMap API
# ------------------------------------------------------------------------------

OPENWEATHERMAP_API_KEY = os.environ.get(
    "OPENWEATHERMAP_API_KEY",
    ""
)


# ------------------------------------------------------------------------------
# Email settings
# ------------------------------------------------------------------------------

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST",
    "smtp.gmail.com"
)

EMAIL_PORT = int(
    os.environ.get(
        "EMAIL_PORT",
        "587"
    )
)

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    ""
)

DEFAULT_FROM_EMAIL = (
    EMAIL_HOST_USER
    or "noreply@travelwebsite.local"
)


# ------------------------------------------------------------------------------
# Django message tags
# ------------------------------------------------------------------------------

MESSAGE_TAGS = {
    10: "debug",
    20: "info",
    25: "success",
    30: "warning",
    40: "danger",
}


# ------------------------------------------------------------------------------
# Production security settings
# ------------------------------------------------------------------------------
#
# These are enabled only when DEBUG=False.
# They help protect the deployed application.
# ------------------------------------------------------------------------------

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = "same-origin"

    X_FRAME_OPTIONS = "DENY"