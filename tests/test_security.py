"""
Security headers test untuk RDP Starter Kit.
US: US-016 — Security headers production-ready

TUJUAN: Verifikasi security settings production-ready.

ALUR:
  1. Test production settings punya flag yang benar
  2. Test development settings tidak redirect HTTPS (agar local dev jalan)
  3. Test --deploy check tidak ada warning kritis

DIPANGGIL DARI: uv run pytest tests/test_security.py
DEPENDENSI: django.test, django.conf.settings
"""

from django.test import TestCase, override_settings


class TestProductionSecuritySettings(TestCase):
    """
    TUJUAN: Verify production settings memenuhi AC US-016.

    US: US-016 — Security headers production-ready
    """

    def _get_production_settings(self):
        """Load production settings module dan return sebagai dict."""
        # Import production module langsung (bukan via DJANGO_SETTINGS_MODULE)
        import config.settings.production as prod

        return prod

    def test_debug_false_in_production(self):
        """AC: production.py harus set DEBUG=False."""
        prod = self._get_production_settings()
        assert prod.DEBUG is False, "DEBUG harus False di production settings"

    def test_ssl_redirect_enabled(self):
        """AC: SECURE_SSL_REDIRECT harus True di production."""
        prod = self._get_production_settings()
        assert prod.SECURE_SSL_REDIRECT is True

    def test_session_cookie_secure(self):
        """AC: SESSION_COOKIE_SECURE harus True di production."""
        prod = self._get_production_settings()
        assert prod.SESSION_COOKIE_SECURE is True

    def test_csrf_cookie_secure(self):
        """AC: CSRF_COOKIE_SECURE harus True di production."""
        prod = self._get_production_settings()
        assert prod.CSRF_COOKIE_SECURE is True

    def test_hsts_enabled(self):
        """AC: HSTS harus dikonfigurasi dengan durasi >= 1 tahun."""
        prod = self._get_production_settings()
        assert prod.SECURE_HSTS_SECONDS >= 31536000, (
            f"HSTS harus >= 31536000 (1 tahun), dapat: {prod.SECURE_HSTS_SECONDS}"
        )

    def test_hsts_include_subdomains(self):
        """AC: HSTS harus mencakup subdomain."""
        prod = self._get_production_settings()
        assert prod.SECURE_HSTS_INCLUDE_SUBDOMAINS is True

    def test_x_frame_options_deny(self):
        """AC: X-Frame-Options harus DENY (anti-clickjacking)."""
        prod = self._get_production_settings()
        assert prod.X_FRAME_OPTIONS == "DENY"

    def test_content_type_nosniff(self):
        """AC: SECURE_CONTENT_TYPE_NOSNIFF harus True."""
        prod = self._get_production_settings()
        assert prod.SECURE_CONTENT_TYPE_NOSNIFF is True

    def test_referrer_policy_set(self):
        """AC: SECURE_REFERRER_POLICY harus dikonfigurasi."""
        prod = self._get_production_settings()
        assert hasattr(prod, "SECURE_REFERRER_POLICY"), (
            "SECURE_REFERRER_POLICY harus ada di production settings"
        )
        assert prod.SECURE_REFERRER_POLICY, "SECURE_REFERRER_POLICY tidak boleh kosong"

    def test_no_fake_csp_setting(self):
        """
        Verifikasi SECURE_CONTENT_SECURITY_POLICY (setting palsu) tidak ada.
        Django tidak punya built-in CSP support — setting ini tidak berfungsi.
        """
        prod = self._get_production_settings()
        assert not hasattr(prod, "SECURE_CONTENT_SECURITY_POLICY"), (
            "SECURE_CONTENT_SECURITY_POLICY bukan setting Django bawaan. "
            "Hapus dan gunakan django-csp jika butuh CSP header."
        )


class TestDevelopmentSecuritySettings(TestCase):
    """
    TUJUAN: Verify dev settings TIDAK mengaktifkan HTTPS redirect.

    US: US-016 AC: dev settings tidak ganggu local dev
    """

    def _get_dev_settings(self):
        import config.settings.dev as dev

        return dev

    def test_ssl_redirect_disabled_in_dev(self):
        """AC: SECURE_SSL_REDIRECT harus False di dev (lokal tidak pakai HTTPS)."""
        dev = self._get_dev_settings()
        assert dev.SECURE_SSL_REDIRECT is False

    def test_debug_true_in_dev(self):
        """AC: DEBUG harus True di dev."""
        dev = self._get_dev_settings()
        assert dev.DEBUG is True

    def test_csrf_cookie_not_secure_in_dev(self):
        """AC: CSRF_COOKIE_SECURE False di dev (localhost tidak HTTPS)."""
        dev = self._get_dev_settings()
        assert dev.CSRF_COOKIE_SECURE is False


class TestSecurityHeadersInResponse(TestCase):
    """
    TUJUAN: Verify response header X-Frame-Options dan X-Content-Type-Options
            muncul saat settings dikonfigurasi.

    Catatan: HSTS dan SSL redirect tidak bisa ditest via test client karena
    perlu HTTPS transport nyata. Test di sini cover header level-Django.
    US: US-016
    """

    @override_settings(X_FRAME_OPTIONS="DENY", SECURE_CONTENT_TYPE_NOSNIFF=True)
    def test_x_frame_options_header_in_response(self):
        """X-Frame-Options: DENY harus ada di setiap response."""
        response = self.client.get("/dashboard/")
        # Response bisa 200 atau 302 (redirect ke login) — yang penting header ada
        assert response.status_code in [200, 302]
        # X-Frame-Options di-set oleh XFrameOptionsMiddleware
        assert "X-Frame-Options" in response, (
            "Header X-Frame-Options tidak ditemukan. "
            "Pastikan XFrameOptionsMiddleware ada di MIDDLEWARE."
        )
        assert response["X-Frame-Options"] == "DENY"

    @override_settings(SECURE_CONTENT_TYPE_NOSNIFF=True)
    def test_content_type_nosniff_header(self):
        """X-Content-Type-Options: nosniff harus ada di setiap response."""
        response = self.client.get("/dashboard/")
        assert response.status_code in [200, 302]
        assert "X-Content-Type-Options" in response, (
            "Header X-Content-Type-Options tidak ditemukan. "
            "Pastikan SecurityMiddleware ada di MIDDLEWARE."
        )
        assert response["X-Content-Type-Options"] == "nosniff"
