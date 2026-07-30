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

import json
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
RDP_DEBUG_OVERLAY = env_var("RDP_DEBUG_OVERLAY", str(DEBUG)).lower() in ("true", "1", "yes")

# ⚙️ KONFIGURASI: RDP-UI Version and Self-Host
RDP_UI_VERSION = env_var("RDP_UI_VERSION", "v1.0")
RDP_UI_SELF_HOST = env_var("RDP_UI_SELF_HOST", "False").lower() in ("true", "1", "yes")
RDP_APP_ACCENT = env_var("RDP_APP_ACCENT", "navy")

# ⚙️ KONFIGURASI: Framework & App Versions
FRAMEWORK_VERSION = env_var("FRAMEWORK_VERSION", "0.3.0")

_version_file = BASE_DIR / "config" / "version.json"
LOCAL_APP_VERSION = "1.0.0"
LOCAL_APP_VERSION_DATE = ""
LOCAL_APP_VERSION_BY = "System"
LOCAL_APP_VERSION_DESC = ""

if _version_file.exists():
    try:
        with open(_version_file, "r") as f:
            _v_data = json.load(f)
            LOCAL_APP_VERSION = _v_data.get("version", LOCAL_APP_VERSION)
            LOCAL_APP_VERSION_DATE = _v_data.get("updated_at", "")
            LOCAL_APP_VERSION_BY = _v_data.get("updated_by", "System")
            LOCAL_APP_VERSION_DESC = _v_data.get("description", "")
    except Exception:
        pass


# ⚙️ KONFIGURASI: White label — brand bisa dikustom via .env
SITE_NAME = env_var("SITE_NAME", "RDP Starter Kit")
COMPANY_NAME = env_var("COMPANY_NAME", "Radian Data Platform")
APP_BRAND_SHORT = env_var("APP_BRAND_SHORT", "RDP")
COPYRIGHT_YEAR = env_var("COPYRIGHT_YEAR", "2026")

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
            "❌ Invalid DATABASE_URL format. Expected: "
            "postgresql://user:password@host:port/dbname or sqlite:///path/to/db.sqlite3"
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
    # US-012: jazzmin harus sebelum django.contrib.admin
    "jazzmin",
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
    "drf_spectacular",
    "storages",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.inventory.apps.InventoryConfig",
    "apps.test_app.apps.TestAppConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



# ⚙️ KONFIGURASI: Custom User model
AUTH_USER_MODEL = "accounts.User"

# ⚙️ KONFIGURASI: Custom Authentication Backend (Support Email/Username Login)
AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ⚙️ KONFIGURASI: US-012 — Jazzmin admin theme
# KEPUTUSAN TEKNIS: Pakai jazzmin untuk tema admin kustom
# ALASAN: Tampilan lebih modern, dark mode otomatis via OS, tanpa perlu override template manual
# ALTERNATIF: Override template admin secara manual (lebih kontrol tapi effort besar)
JAZZMIN_SETTINGS = {
    "site_title": f"{APP_BRAND_SHORT} Admin",
    "site_header": COMPANY_NAME,
    "site_brand": APP_BRAND_SHORT,
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": f"Selamat datang di {APP_BRAND_SHORT} Admin",
    "copyright": COMPANY_NAME,
    # Search model — shortcut search di navbar admin
    "search_model": ["accounts.User"],
    # Top menu links
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "App", "url": "/", "new_window": False},
    ],
    # User menu (kanan atas)
    "usermenu_links": [
        {"name": "Profil", "url": "/accounts/profile/", "new_window": False},
    ],
    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    # Icon per model — Font Awesome 5 Free
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user",
        "accounts.UserProfile": "fas fa-id-card",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # UI tweaks
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": False,  # pakai CDN jazzmin bawaan, bukan Google Fonts
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    # KEPUTUSAN TEKNIS: theme "darkly" untuk dark mode, "flatly" untuk light mode
    # ALASAN: User bisa ganti via admin UI builder kalau show_ui_builder=True
    # Pakai "auto" tidak tersedia di jazzmin — dark mode via bootswatch theme
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    # 🧪 TEST MANUAL: Theme bisa diubah ke "flatly" untuk light mode
    "theme": "darkly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
# KEPUTUSAN TEKNIS: Custom User sejak awal (bukan Django default User)
# ALASAN: Memudahkan menambah field ke User di masa depan tanpa migrasi berbahaya
# ALTERNATIF: Pakai Django default User (kurang flexible)

# ⚙️ KONFIGURASI: Registration wizard steps — dikonfigurasi via .env
# Format JSON: [{"key":"org","label":"Organisasi","type":"text","required":true}]
# Tipe field: text, email, select (butuh "choices": [...]), textarea
# Default kosong = wizard hanya email + password
REGISTRATION_STEPS = json.loads(env_var("REGISTRATION_STEPS", "[]"))

# ⚙️ KONFIGURASI: US-008 — Wajib verifikasi email sebelum akses penuh
# False = user bisa langsung akses semua fitur walau belum verify
# True  = user diarahkan ke halaman "cek email" jika belum verify
REQUIRE_EMAIL_VERIFICATION = env_var("REQUIRE_EMAIL_VERIFICATION", "False").lower() == "true"

# ⚙️ KONFIGURASI: Auth URL — @login_required redirect ke sini
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # US-008: Enforce email verification jika REQUIRE_EMAIL_VERIFICATION=True
    "apps.core.middleware.EmailVerificationMiddleware",
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
                "apps.core.context_processors.debug_settings",
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ⚙️ KONFIGURASI: API Documentation (drf-spectacular)
SPECTACULAR_SETTINGS = {
    "TITLE": f"{APP_BRAND_SHORT} API",
    "DESCRIPTION": f"Dokumentasi API untuk {COMPANY_NAME}",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Menghapus endpoints dari format schema yang tidak perlu
    "COMPONENT_SPLIT_REQUEST": True,
}

# ⚙️ KONFIGURASI: Celery
# KEPUTUSAN TEKNIS: Redis sebagai broker dan result backend.
CELERY_BROKER_URL = env_var("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env_var("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ⚙️ KONFIGURASI: Django-Cotton
COTTON_COMPONENTS_DIR = "templates/cotton"

logger = logging.getLogger(__name__)

# ⚙️ KONFIGURASI: Cloud Storage (S3 / MinIO)
USE_S3 = env_var("USE_S3", "False").lower() in ("true", "1", "yes")
if USE_S3:
    # Konfigurasi django-storages
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = env_var("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = env_var("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = env_var("AWS_STORAGE_BUCKET_NAME", "")
    AWS_S3_ENDPOINT_URL = env_var("AWS_S3_ENDPOINT_URL", None) # Untuk MinIO/R2
    AWS_S3_REGION_NAME = env_var("AWS_S3_REGION_NAME", None)
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = env_var("AWS_S3_VERIFY", "True").lower() in ("true", "1", "yes") # Set False jika pakai MinIO localhost tanpa SSL

