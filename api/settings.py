from pathlib import Path
from decouple import config
from kombu import Exchange, Queue
from datetime import timedelta

import os
import psutil
import sys

AUTH_USER_MODEL = "user.User"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "simple_history",  # History
    "drf_yasg",  # Swagger
    "whitenoise.runserver_nostatic",
    "corsheaders",
    "rest_framework_simplejwt",  # Auth
    "rest_framework_simplejwt.token_blacklist",  # Auth
    # APPS:
    "apps.user",
    ###
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Custom middlewares
    "core.middlewares.remove_www_authenticate.RemoveWWWAuthenticateHeaderMiddleware",
    ###
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", cast=str),
        "USER": config("DB_USER", cast=str),
        "PASSWORD": config("DB_PASSWORD", cast=str),
        "HOST": config("DB_HOST", cast=str),
        "PORT": config("DB_PORT", cast=str),
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=0, cast=int),
        "POOL_SIZE": config("DB_POOL_SIZE", default=5, cast=int),
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "OPTIONS": (
            {
                "options": "-c search_path={}".format(config("DB_SCHEMA", cast=str)),
                "sslmode": config("DB_SSL_MODE", default="disable", cast=str),
            }
            if "test" not in sys.argv
            else {}
        ),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_URL = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DISABLE_COLLECTSTATIC = 1

# Media configuration
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", cast=str)
AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com"
AWS_S3_REGION_NAME = "nyc3"
AWS_DEFAULT_ACL = "public-read"

PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com/"
DEFAULT_FILE_STORAGE = "core.storage.PublicMediaStorage"

PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "core.storage.PrivateMediaStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "core.permissions.AccessPermission",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authenticate.CustomAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 20,
}

# Auth JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),
    # Cookies
    "AUTH_COOKIE": "access",
    "AUTH_COOKIE_REFRESH": "refresh",
    "AUTH_COOKIE_DOMAIN": config("COOKIE_DOMAIN", cast=str),
    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_SAMESITE": "None",
}

# CORS configuration
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-xsrf-token",
    # Custom
    ###
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# CSRF configuration
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_DOMAIN = config("COOKIE_DOMAIN", cast=str)

# Session configuration
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_DOMAIN = config("COOKIE_DOMAIN", cast=str)

# Celery configuration
CELERY_BROKER_URL = config("CELERY_BROKER_URL", cast=str)
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", cast=str)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_BROKER_POOL_LIMIT = None
CELERY_BROKER_HEARTBEAT = 10
CELERY_BROKER_CONNECTION_TIMEOUT = 30
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

CELERY_QUEUES = (
    Queue(
        "api_processing",
        Exchange("api_processing"),
        routing_key="api_processing",
    ),
)
CELERY_DEFAULT_QUEUE = "api_processing"
CELERY_DEFAULT_EXCHANGE = "api_processing"
CELERY_DEFAULT_ROUTING_KEY = "api_processing"

NUM_CONTAINERS = config("CELERY_NUM_CONTAINERS", default=1, cast=int)
CPU_CORE_MULTIPLIER = config("CELERY_CPU_CORE_MULTIPLIER", default=1, cast=int)
CPU_COUNT = psutil.cpu_count()
RAW_CONCURRENCY = (CPU_COUNT * CPU_CORE_MULTIPLIER) / NUM_CONTAINERS
CELERY_WORKER_CONCURRENCY = max(1, round(RAW_CONCURRENCY))

# Swagger configuration
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {},
    "USE_SESSION_AUTH": False,
    "DOC_EXPANSION": "none",
    "OPERATIONS_SORTER": "alpha",
    "SHOW_REQUEST_HEADERS": True,
    "PERSIST_AUTH": True,
    "DISPLAY_OPERATION_ID": True,
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "debug.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "api": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Gzip configuration
GZIP_MIN_LENGTH = 500

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", cast=str),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
CACHE_TTL = config("CACHE_TIMEOUT", default=900, cast=int)
