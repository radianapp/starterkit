"""
Django settings untuk production.
US: US-016 — Security headers production-ready
US: US-002 — Konfigurasi environment via `.env`

TUJUAN: Override base settings dengan security headers dan production-grade configuration.
"""

from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = env_var("ALLOWED_HOSTS", "localhost").split(",")  # noqa: F405

# ⚙️ KONFIGURASI: Security headers
# Referensi: https://docs.djangoproject.com/en/stable/ref/settings/#security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "cdn.radian.web.id"),
    "style-src": ("'self'", "'unsafe-inline'", "cdn.radian.web.id"),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "cdn.radian.web.id"),
    "connect-src": ("'self'",),
}
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# ⚙️ KONFIGURASI: Use PostgreSQL di production
# Database sudah dikonfigurasi di base.py dengan DATABASE_URL
# Pastikan DATABASE_URL menunjuk ke PostgreSQL production database

# ⚙️ KONFIGURASI: Cache backend untuk production
# Gunakan Redis untuk production — CACHE_URL di .env harus postgresql://...
# Contoh: CACHE_URL=redis://redis.example.com:6379/0

# ⚙️ KONFIGURASI: Email backend untuk production
# EMAIL_BACKEND harus SMTP di production
# Pastikan EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD di .env

# ⚙️ KONFIGURASI: WhiteNoise untuk serving static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ⚙️ KONFIGURASI: Disable debug toolbar
if "debug_toolbar" in INSTALLED_APPS:  # noqa: F405
    INSTALLED_APPS.remove("debug_toolbar")  # noqa: F405
if "debug_toolbar.middleware.DebugToolbarMiddleware" in MIDDLEWARE:  # noqa: F405
    MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# Log level di production — hanya ERROR dan WARNING
LOGGING["loggers"]["django"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "WARNING"  # noqa: F405
LOGGING["handlers"]["console"]["level"] = "WARNING"  # noqa: F405

print("[OK] Production settings loaded (DEBUG=False, security headers active)")
