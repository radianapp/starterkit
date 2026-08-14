"""
Django Management Command: audit_security
----------------------------------------
Melakukan audit otomatis terhadap konfigurasi keamanan, security headers, cookie flags, dan proteksi views.

Usage:
    python manage.py audit_security
"""

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Melakukan audit keamanan otomatis dan pelaporan skor konfigurasi security."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("🔒 Security & Compliance Audit Report"))
        self.stdout.write("=" * 60)

        pass_count = 0
        warn_count = 0
        fail_count = 0

        # Check 1: Secret Key
        if "change-this" in settings.SECRET_KEY or settings.SECRET_KEY == "your-super-secret-key":
            self._print_check(
                "SECRET_KEY Strength", "FAIL", "Menggunakan Secret Key default yang berbahaya!"
            )
            fail_count += 1
        elif len(settings.SECRET_KEY) < 32:
            self._print_check(
                "SECRET_KEY Strength", "WARN", "SECRET_KEY terlalu pendek (<32 karakter)."
            )
            warn_count += 1
        else:
            self._print_check("SECRET_KEY Strength", "PASS", "SECRET_KEY acak dan cukup panjang.")
            pass_count += 1

        # Check 2: Debug Mode
        if settings.DEBUG:
            self._print_check(
                "DEBUG Mode", "WARN", "DEBUG=True aktif. Pastikan di-set False untuk production."
            )
            warn_count += 1
        else:
            self._print_check("DEBUG Mode", "PASS", "DEBUG=False (Production ready).")
            pass_count += 1

        # Check 3: HTTPS & Cookies Security
        if getattr(settings, "SESSION_COOKIE_SECURE", False):
            self._print_check("Session Cookie Secure", "PASS", "SESSION_COOKIE_SECURE=True.")
            pass_count += 1
        else:
            self._print_check(
                "Session Cookie Secure", "WARN", "SESSION_COOKIE_SECURE belum di-set True."
            )
            warn_count += 1

        if getattr(settings, "CSRF_COOKIE_SECURE", False):
            self._print_check("CSRF Cookie Secure", "PASS", "CSRF_COOKIE_SECURE=True.")
            pass_count += 1
        else:
            self._print_check("CSRF Cookie Secure", "WARN", "CSRF_COOKIE_SECURE belum di-set True.")
            warn_count += 1

        # Check 4: Clickjacking Protection
        if "django.middleware.clickjacking.XFrameOptionsMiddleware" in settings.MIDDLEWARE:
            self._print_check("Clickjacking Middleware", "PASS", "XFrameOptionsMiddleware aktif.")
            pass_count += 1
        else:
            self._print_check(
                "Clickjacking Middleware", "FAIL", "XFrameOptionsMiddleware tidak ditemukan!"
            )
            fail_count += 1

        # Check 5: Multi-Tenancy Setting Status
        is_mt_enabled = getattr(settings, "RDP_MULTI_TENANCY_ENABLED", False)
        self._print_check(
            "Multi-Tenancy Status", "INFO", f"RDP_MULTI_TENANCY_ENABLED = {is_mt_enabled}"
        )

        self.stdout.write("=" * 60)
        self.stdout.write(
            f"Hasil Audit: {pass_count} Passed, {warn_count} Warnings, {fail_count} Failed."
        )
        if fail_count > 0:
            self.stdout.write(
                self.style.ERROR("⚠️ Ditemukan masalah keamanan yang wajib diperbaiki!")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("[OK] Konfigurasi keamanan memenuhi standar baseline.")
            )

    def _print_check(self, title, status, details):
        if status == "PASS":
            tag = self.style.SUCCESS("[PASS]")
        elif status == "WARN":
            tag = self.style.WARNING("[WARN]")
        elif status == "FAIL":
            tag = self.style.ERROR("[FAIL]")
        else:
            tag = self.style.NOTICE("[INFO]")

        self.stdout.write(f"{tag} {title:<25} : {details}")
