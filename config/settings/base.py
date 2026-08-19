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
from pathlib import Path

import environ
from django.contrib.messages import constants as messages

# ⚙️ KONFIGURASI: Load .env file
env = environ.Env()


# ⚙️ KONFIGURASI: Build paths di dalam project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Read .env file
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    environ.Env.read_env(_env_file)

# ⚙️ KONFIGURASI: Django security dan environment
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost,127.0.0.1"])
ENVIRONMENT = env("ENVIRONMENT", default="development")
RDP_DEBUG_OVERLAY = env.bool("RDP_DEBUG_OVERLAY", default=DEBUG)

# ⚙️ KONFIGURASI: RDP-UI Version and Self-Host
RDP_UI_VERSION = env("RDP_UI_VERSION", default="v1.0")
RDP_UI_SELF_HOST = env.bool("RDP_UI_SELF_HOST", default=False)
RDP_APP_ACCENT = env("RDP_APP_ACCENT", default="navy")
RDP_MULTI_TENANCY_ENABLED = env("RDP_MULTI_TENANCY_ENABLED", default="False").lower() in (
    "true",
    "1",
    "yes",
)

# ⚙️ KONFIGURASI: Framework & App Versions
FRAMEWORK_VERSION = env("FRAMEWORK_VERSION", default="0.7.0")

_version_file = BASE_DIR / "config" / "version.json"
LOCAL_APP_VERSION = "1.0.0"
LOCAL_APP_VERSION_DATE = ""
LOCAL_APP_VERSION_BY = "System"
LOCAL_APP_VERSION_DESC = ""

if _version_file.exists():
    try:
        with open(_version_file) as f:
            _v_data = json.load(f)
            LOCAL_APP_VERSION = _v_data.get("version", LOCAL_APP_VERSION)
            LOCAL_APP_VERSION_DATE = _v_data.get("updated_at", "")
            LOCAL_APP_VERSION_BY = _v_data.get("updated_by", "System")
            LOCAL_APP_VERSION_DESC = _v_data.get("description", "")
    except Exception:
        pass


# ⚙️ KONFIGURASI: White label — brand bisa dikustom via .env
SITE_NAME = env("SITE_NAME", default="RDP Starter Kit")
COMPANY_NAME = env("COMPANY_NAME", default="Radian Data Platform")
APP_BRAND_SHORT = env("APP_BRAND_SHORT", default="RDP")
COPYRIGHT_YEAR = env("COPYRIGHT_YEAR", default="2026")

# ⚙️ KONFIGURASI: Database
DEFAULT_DB_ENGINE = "django.db.backends.sqlite3" if DEBUG else "django.db.backends.postgresql"
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///" + str(BASE_DIR / "db.sqlite3"))}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=600)

# ⚙️ KONFIGURASI: Cache backend
CACHES = {"default": env.cache("CACHE_URL", default="locmemcache://rdp-starter-locmem")}


# ⚙️ KONFIGURASI: Email backend
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@radianapp.com")

# KEPUTUSAN TEKNIS: Integrasi django-anymail
ANYMAIL_PROVIDER = env("ANYMAIL_PROVIDER", default="")
if ANYMAIL_PROVIDER:
    EMAIL_BACKEND = (
        "anymail.backends.mailgun.EmailBackend"
        if ANYMAIL_PROVIDER == "mailgun"
        else f"anymail.backends.{ANYMAIL_PROVIDER}.EmailBackend"
    )
    ANYMAIL = {
        "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default=""),
        "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN", default=""),
        "SENDGRID_API_KEY": env("SENDGRID_API_KEY", default=""),
        "RESEND_API_KEY": env("RESEND_API_KEY", default=""),
    }
elif EMAIL_BACKEND == "mailpit":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False
elif EMAIL_BACKEND == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_BACKEND == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

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
    "simple_history",
    "anymail",
    "django_celery_beat",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.inventory.apps.InventoryConfig",
    "apps.tenants.apps.TenantsConfig",
    "apps.test_app.apps.TestAppConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ⚙️ KONFIGURASI: Custom User model
AUTH_USER_MODEL = "accounts.User"

# ⚙️ KONFIGURASI: Custom Authentication Backend (Support Email/Username Login)
AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
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
    "default_theme_mode": "auto",
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
REGISTRATION_STEPS = json.loads(env("REGISTRATION_STEPS", default="[]"))

# ⚙️ KONFIGURASI: US-008 — Wajib verifikasi email sebelum akses penuh
# False = user bisa langsung akses semua fitur walau belum verify
# True  = user diarahkan ke halaman "cek email" jika belum verify
REQUIRE_EMAIL_VERIFICATION = env("REQUIRE_EMAIL_VERIFICATION", default="False").lower() == "true"

# ⚙️ KONFIGURASI: Auth & Registration Features
ENABLE_USER_REGISTRATION = env("ENABLE_USER_REGISTRATION", default="True").lower() in (
    "true",
    "1",
    "yes",
)
ENABLE_GOOGLE_AUTH = env.bool("ENABLE_GOOGLE_AUTH", default=False)
ENABLE_2FA = env.bool("ENABLE_2FA", default=True)
REQUIRE_2FA = env.bool("REQUIRE_2FA", default=False)

# ⚙️ KONFIGURASI: Domain Whitelist untuk Registrasi
_allowed_domains_env = env("ALLOWED_EMAIL_DOMAINS", default="")
ALLOWED_EMAIL_DOMAINS = [
    domain.strip().lower() for domain in _allowed_domains_env.split(",") if domain.strip()
]

# ⚙️ KONFIGURASI: Custom Account Adapter untuk django-allauth
# Digunakan untuk menerapkan batasan domain (dan lain-lain) saat login via Google SSO
ACCOUNT_ADAPTER = "apps.accounts.adapters.DomainRestrictAdapter"

# ⚙️ KONFIGURASI: Audit Trail
ENABLE_AUDIT_TRAIL = env.bool("ENABLE_AUDIT_TRAIL", default=True)

# ⚙️ KONFIGURASI: Auth URL — @login_required redirect ke sini
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ⚙️ KONFIGURASI: Django-Allauth (SSO)
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"  # RDP menggunakan logic verifikasi kustom
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID", default=""),
            "secret": env("GOOGLE_CLIENT_SECRET", default=""),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}

MIDDLEWARE = [
    "apps.core.middleware.TraceMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Multi-Tenancy Middleware (bypasses if RDP_MULTI_TENANCY_ENABLED=False)
    "apps.tenants.middleware.tenant_middleware.TenantMiddleware",
    # US-008: Enforce email verification jika REQUIRE_EMAIL_VERIFICATION=True
    "apps.core.middleware.EmailVerificationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Force password change for bulk uploaded users
    "apps.accounts.middleware.ForceChangePasswordMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# KEPUTUSAN TEKNIS: Map Django message tags 'error' ke 'danger' agar sesuai dengan standar CSS alert
MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

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
cors_origins = env("CORS_ALLOWED_ORIGINS", default="")
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
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ⚙️ KONFIGURASI: Django-Cotton
COTTON_COMPONENTS_DIR = "templates/cotton"

logger = logging.getLogger(__name__)

# ⚙️ KONFIGURASI: Cloud Storage (S3 / MinIO)
USE_S3 = env.bool("USE_S3", default=False)
if USE_S3:
    # Konfigurasi django-storages
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default=None)  # Untuk MinIO/R2
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default=None)
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = env.bool(
        "AWS_S3_VERIFY", default=True
    )  # Set False jika pakai MinIO localhost tanpa SSL

# ⚙️ KONFIGURASI: Cloudflare Turnstile (CAPTCHA)
TURNSTILE_ENABLED = env.bool("TURNSTILE_ENABLED", default=False)
# Default keys provided are dummy keys for testing that always pass
TURNSTILE_SITE_KEY = env("TURNSTILE_SITE_KEY", default="1x00000000000000000000AA")
TURNSTILE_SECRET_KEY = env("TURNSTILE_SECRET_KEY", default="1x0000000000000000000000000000000AA")
