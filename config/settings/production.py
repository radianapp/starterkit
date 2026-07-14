"""
Django settings untuk production.
US: US-016 — Security headers production-ready
US: US-002 — Konfigurasi environment via `.env`

TUJUAN: Override base settings dengan security headers dan production-grade configuration.

## CARA KERJA
Security headers dikonfigurasi via Django built-in settings:
  - HTTPS: SECURE_SSL_REDIRECT + HSTS (SECURE_HSTS_SECONDS)
  - Cookie: SESSION_COOKIE_SECURE + CSRF_COOKIE_SECURE
  - Clickjacking: X_FRAME_OPTIONS = DENY
  - MIME sniff: SECURE_CONTENT_TYPE_NOSNIFF
  - Referrer: SECURE_REFERRER_POLICY
  - CSP: belum diterapkan di v0.2 — butuh package `django-csp`.
          Roadmap v0.3+. Header CSP saat ini dikelola di level nginx/reverse-proxy.
"""

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = env_var("ALLOWED_HOSTS", "localhost").split(",")  # noqa: F405

# ⚙️ KONFIGURASI: HTTPS redirect + cookie security
# Referensi: https://docs.djangoproject.com/en/stable/ref/settings/#security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ⚙️ KONFIGURASI: HTTP Strict Transport Security (HSTS)
# KEPUTUSAN TEKNIS: 1 tahun + includeSubDomains + preload
# ALASAN: Setelah HSTS aktif dengan preload, domain terdaftar di browser preload list
# ⚠️ PERHATIAN: Jangan aktifkan di production sebelum HTTPS benar-benar berjalan
#               HSTS tidak bisa di-undo dengan mudah setelah browser cache-nya
SECURE_HSTS_SECONDS = 31536000  # 1 tahun
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ⚙️ KONFIGURASI: Anti-clickjacking + MIME sniff prevention
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# ⚙️ KONFIGURASI: Referrer policy
# KEPUTUSAN TEKNIS: strict-origin-when-cross-origin
# ALASAN: Masih mengirim referrer untuk same-origin (analytics internal), tapi
#         tidak bocorkan path ke domain lain
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# KEPUTUSAN TEKNIS: CSP tidak dikonfigurasi via Django di v0.2
# ALASAN: Django tidak punya built-in CSP support. Butuh `django-csp` (roadmap v0.3).
#         Saat ini CSP dikelola di nginx/reverse-proxy config.
# ALTERNATIF: uv add django-csp → tambah 'csp' ke INSTALLED_APPS + CSP_* settings

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
