"""
Django settings for reboot project.

Production-aware: secrets and environment-specific config are read from
environment variables. See .env.example for required variables.
"""

from pathlib import Path
from datetime import timedelta

import dj_database_url
from decouple import config, Csv


BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# SECURITY & ENVIRONMENT
# ---------------------------------------------------------------------------

# Secret key MUST come from env. Never hardcode in production.
SECRET_KEY = config('SECRET_KEY')

# DEBUG defaults to False — has to be explicitly turned on per-environment.
# This is the safer default: forgetting to set DEBUG can't expose stack traces.
DEBUG = config('DEBUG', default='False') == 'True'

# ALLOWED_HOSTS comma-separated in env var, parsed into a list here.
# Django refuses connections from any host not in this list (for HTTP Host
# header attacks). Locally: 'localhost,127.0.0.1'. In prod: your domain.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
]

AUTH_USER_MODEL = 'accounts.User'


# ---------------------------------------------------------------------------
# APPS
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "accounts.apps.AccountsConfig",
    "concepts.apps.ConceptsConfig",
    "mentorship.apps.MentorshipConfig",
    "notifications.apps.NotificationsConfig",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "api",
    "trends",
    "buddy",
]


# ---------------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------------
# Order matters here. Notable additions for production:
#   - CorsMiddleware (already had this) must come BEFORE CommonMiddleware
#   - WhiteNoiseMiddleware must come right after SecurityMiddleware

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",            # ← NEW: serves static files in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ---------------------------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# ---------------------------------------------------------------------------
# URLS / TEMPLATES / WSGI
# ---------------------------------------------------------------------------

ROOT_URLCONF = "reboot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'notifications.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = "reboot.wsgi.application"


# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------
# dj_database_url.config() parses DATABASE_URL from env into Django's format.
# Locally: DATABASE_URL=sqlite:///db.sqlite3 (your existing SQLite db)
# In prod: DATABASE_URL=postgres://... (Render provisions this automatically)
#
# conn_max_age keeps connections alive for 10 minutes between requests,
# avoiding the cost of reconnecting on every API call.

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
    )
}


# ---------------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------
# STATIC_URL — URL prefix where static files are served.
# STATICFILES_DIRS — your source folders for static files (your own assets).
# STATIC_ROOT — where `collectstatic` will gather everything for production.
# STORAGES — tells Django to use WhiteNoise with compression+caching in prod.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ---------------------------------------------------------------------------
# MEDIA
# ---------------------------------------------------------------------------
# Note: on Render's free tier, local filesystem media is EPHEMERAL — files
# uploaded after deploy disappear on next deploy. For now we leave it as-is;
# v2 enhancement is moving uploads to S3 or Cloudinary.

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# Locally: http://localhost:3000
# In prod: https://your-frontend.onrender.com (set via env var)

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000',
    cast=Csv(),
)

# Anthropic API key for AI Career Buddy
ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')

# ---------------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# PRODUCTION-ONLY SECURITY HEADERS
# ---------------------------------------------------------------------------
# Enabled only when SECURE_HTTPS is true. Don't flip this on locally —
# it forces HTTPS redirects that runserver can't honour.

SECURE_HTTPS = config('SECURE_HTTPS', default='False') == 'True'

if SECURE_HTTPS:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True