"""
Django settings untuk development.
US: US-002 — Konfigurasi environment via `.env`

TUJUAN: Override production settings dengan setup yang cocok untuk development lokal.
"""

from .base import *  # noqa: F403

RDP_DEBUG_OVERLAY = env_var("RDP_DEBUG_OVERLAY", "True").lower() in ("true", "1", "yes")

# For local development of the UI framework, ensure we load local CSS
RDP_UI_SELF_HOST = True

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Email backend sudah default console di base.py — tidak perlu override

# Development cache — gunakan local memory
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "rdp-starter-locmem",
    }
}

# Django Debug Toolbar untuk development
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1"]

# Log level lebih verbose di development
LOGGING["loggers"]["django"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405

# KEPUTUSAN TEKNIS: CSRF tidak perlu secure di development
# ALASAN: localhost tidak pakai HTTPS
# ALTERNATIF: Enable di production
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

print("[OK] Development settings loaded (DEBUG=True, SQLite, console email)")
