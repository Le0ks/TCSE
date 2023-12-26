from pathlib import Path

import django.contrib.messages
from dotenv import dotenv_values

config = dotenv_values(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config["SECRET_KEY"] or "YOUR_SECRET_KEY"

DEBUG = (config["DEBUG"] or "False") == "True"

ALLOWED_HOSTS = config["ALLOWED_HOSTS"].split() or "*"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "events.apps.EventsConfig",
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "about.apps.AboutConfig",
    "widget_tweaks",
    "social_django",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

INTERNAL_IPS = config["INTERNAL_IPS"].split() or "127.0.0.1"

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]


LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

USER_IS_ACTIVE = (
    (config["USER_IS_ACTIVE"] or "False") == "True"
)

AUTHENTICATION_BACKENDS = [
    "users.backends.EmailBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.yandex.YandexOAuth2",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config["SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config[
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"
]

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = config["SOCIAL_AUTH_YANDEX_OAUTH2_KEY"]
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = config[
    "SOCIAL_AUTH_YANDEX_OAUTH2_SECRET"
]

SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "users.pipelines.create_profile_for_social_authenticated_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

LOGIN_ATTEMPTS = int(config["LOGIN_ATTEMPTS"]) or 3

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

AUTH_USER_MODEL = "users.User"


if (config["USE_SMTP"] or "False") == "True":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config["EMAIL_HOST"]
    EMAIL_PORT = config["EMAIL_PORT"]
    EMAIL_USE_TLS = (
        (config["EMAIL_USE_TLS"] or "True") == "True"
    )
    EMAIL_USE_SSL = (
        (config["EMAIL_USE_SSL"] or "False") == "True"
    )
    EMAIL_HOST_USER = config["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_ADMIN = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

PASSWORD_RESET_TIMEOUT = 43200

MESSAGE_TAGS = {
    django.contrib.messages.constants.DEBUG: "alert-secondary",
    django.contrib.messages.constants.INFO: "alert-info",
    django.contrib.messages.constants.SUCCESS: "alert-success",
    django.contrib.messages.constants.WARNING: "alert-warning",
    django.contrib.messages.constants.ERROR: "alert-danger",
}
