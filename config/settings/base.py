"""
Django settings untuk RDP Starter Kit.
US: US-001, US-002, US-003

TUJUAN: Konfigurasi dasar Django dengan support environment variables.

ALUR:
  1. Import dotenv dan load .env file
  2. Setup environment variable reader dengan fallback
  3. Configure database, cache, email dari env
  4. Setup INSTALLED_APPS dengan apps custom
  5. Configure authentication dengan Custom User model
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# ⚙️ KONFIGURASI: Load .env file
# Lokasi: root project directory (sejajar manage.py)
load_dotenv()


def env_var(key: str, default=None, required=False):
    """
    TUJUAN: Baca variabel environment dengan validation dan error message yang jelas.

    ALUR:
      1. Ambil nilai dari environment
      2. Jika tidak ada dan required=True, raise ValueError dengan nama variabel
      3. Jika tidak ada dan ada default, return default
      4. Return nilai yang ada

    DIPANGGIL DARI: config/settings/base.py
    DEPENDENSI: os.environ
    """
    value = os.environ.get(key, default)
    if value is None and required:
        raise ValueError(
            f"❌ Environment variable '{key}' is required but not found in .env or environment. "
            f"Please add it to .env file."
        )
    return value


# ⚙️ KONFIGURASI: Build paths di dalam project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ⚙️ KONFIGURASI: Django security dan environment
SECRET_KEY = env_var("SECRET_KEY", required=True)
DEBUG = env_var("DEBUG", "False").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = env_var("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ENVIRONMENT = env_var("ENVIRONMENT", "development")

# ⚙️ KONFIGURASI: Database
DEFAULT_DB_ENGINE = "django.db.backends.sqlite3" if DEBUG else "django.db.backends.postgresql"
DATABASE_URL = env_var(
    "DATABASE_URL",
    "sqlite:///db.sqlite3" if DEBUG else None,
    required=not DEBUG,
)

# KEPUTUSAN TEKNIS: Parse DATABASE_URL untuk Django database config
# ALASAN: DATABASE_URL lebih mudah di-manage di environment daripada DATABASES dict terpisah
# ALTERNATIF: Bisa pakai dj-database-url library untuk parsing yang lebih robust
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / (db_path or "db.sqlite3"),
        }
    }
else:
    # PostgreSQL format: postgresql://user:password@host:port/dbname
    import re

    match = re.match(
        r"postgresql://(?:(\w+):(\w+)@)?([a-z0-9.-]+):(\d+)/([a-z0-9_-]+)",
        DATABASE_URL,
    )
    if not match:
        raise ValueError(
            f"❌ Invalid DATABASE_URL format. Expected: "
            f"postgresql://user:password@host:port/dbname or sqlite:///path/to/db.sqlite3"
        )
    user, password, host, port, dbname = match.groups()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": dbname,
            "USER": user or "postgres",
            "PASSWORD": password or "",
            "HOST": host,
            "PORT": port or "5432",
            "CONN_MAX_AGE": 600,  # Persistent connection pool
        }
    }

# ⚙️ KONFIGURASI: Cache backend
CACHE_URL = env_var("CACHE_URL", "locmem://")
# KEPUTUSAN TEKNIS: Gunakan locmem:// default untuk development
# ALASAN: Tidak perlu install Redis untuk development awal
# ALTERNATIF: redis://localhost:6379/0 untuk production
if CACHE_URL.startswith("redis"):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": CACHE_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "redis.StrictRedis",
            },
            "KEY_PREFIX": "rdp_starter",
            "TIMEOUT": 300,
        }
    }
else:  # locmem://
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "rdp-starter-locmem",
            "OPTIONS": {
                "MAX_ENTRIES": 1000,
            },
            "TIMEOUT": 300,
        }
    }

# ⚙️ KONFIGURASI: Email backend
EMAIL_BACKEND = env_var("EMAIL_BACKEND", "console")
EMAIL_HOST = env_var("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(env_var("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_var("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = env_var("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env_var("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = env_var("DEFAULT_FROM_EMAIL", "noreply@radianapp.com")

# KEPUTUSAN TEKNIS: Support 3 email backend dengan env variable
# ALASAN: Console untuk dev, Mailpit untuk test HTML, SMTP untuk production
# ALTERNATIF: Hardcode ke 1 backend saja (kurang flexible)
if EMAIL_BACKEND == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
elif EMAIL_BACKEND == "mailpit":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False
else:  # console
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "django_cotton",  # django-cotton component framework
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.dashboard.apps.DashboardConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ⚙️ KONFIGURASI: Custom User model
AUTH_USER_MODEL = "accounts.User"
# KEPUTUSAN TEKNIS: Custom User sejak awal (bukan Django default User)
# ALASAN: Memudahkan menambah field ke User di masa depan tanpa migrasi berbahaya
# ALTERNATIF: Pakai Django default User (kurang flexible)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "id-id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ⚙️ KONFIGURASI: Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ⚙️ KONFIGURASI: CORS
cors_origins = env_var("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_origins.split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# ⚙️ KONFIGURASI: Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ⚙️ KONFIGURASI: Django-Cotton
COTTON_COMPONENTS_DIR = "templates/cotton"

logger = logging.getLogger(__name__)
