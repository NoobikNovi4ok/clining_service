import os
from pathlib import Path
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import environ

env = environ.Env()
environ.Env.read_env()  # Читает .env файл

X_FRAME_OPTIONS = "SAMEORIGIN"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-yoarl_-tp#+1lm%t06b$&5vp0js7ku^b5hi1yxyl@m34r+2js%"

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap5",
    "main",
    "users.apps.UsersConfig",
    "clireq.apps.ClireqConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Для локализации
    "django.middleware.locale.LocaleMiddleware",
    #
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clining_service.urls"

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

WSGI_APPLICATION = "clining_service.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation

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

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    # добавьте другие языки по мере необходимости
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

#

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static", "/var/www/static/"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Для перенаправления на авторизацию с помощью декоратора login_required
LOGIN_URL = "user:login"

AUTH_USER_MODEL = "users.CustomUser"
