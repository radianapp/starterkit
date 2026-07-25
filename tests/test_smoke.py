"""
Smoke tests untuk RDP Starter Kit.
US: US-017 — Test suite siap pakai
US: US-001 — Clone & jalankan project baru
US: US-003 — Custom User model siap pakai

TUJUAN: Basic tests untuk memverifikasi project dapat dijalankan tanpa error fundamental.

ALUR:
  1. Test Django dapat di-import dan settings berjalan
  2. Test database migrations dapat dijalankan
  3. Test Custom User model dapat dibuat
  4. Test basic views dapat diakses
"""

import pytest

from apps.accounts.models import User, UserProfile


class TestDjangoSetup:
    """Test Django setup dan configuration."""

    def test_django_settings_loaded(self):
        """
        TUJUAN: Verify Django settings dapat dimuat tanpa error.

        AC: settings.DEBUG harus ada dan bernilai boolean
        """
        from django.conf import settings

        assert hasattr(settings, "DEBUG")
        assert isinstance(settings.DEBUG, bool)

    def test_django_settings_auth_user_model(self):
        """
        TUJUAN: Verify AUTH_USER_MODEL pointing ke Custom User.

        AC: settings.AUTH_USER_MODEL harus sama dengan "accounts.User"
        """
        from django.conf import settings

        assert settings.AUTH_USER_MODEL == "accounts.User"

    def test_installed_apps(self):
        """
        TUJUAN: Verify all required apps di INSTALLED_APPS.

        AC: accounts, core, dashboard harus ada
        """
        from django.conf import settings

        # Extract app labels: apps.accounts.apps.AccountsConfig -> accounts
        app_labels = []
        for app in settings.INSTALLED_APPS:
            if "." in app:
                parts = app.split(".")
                if "apps" in parts:
                    # apps.accounts.apps.AccountsConfig -> accounts
                    app_labels.append(parts[1])
                else:
                    # django.contrib.admin -> admin
                    app_labels.append(parts[-1])
            else:
                app_labels.append(app)

        required_apps = ["accounts", "core", "dashboard"]
        for app in required_apps:
            assert app in app_labels, f"App '{app}' not in INSTALLED_APPS. Found: {app_labels}"


class TestCustomUserModel:
    """Test Custom User model functionality."""

    @pytest.mark.django_db
    def test_user_creation_with_email(self):
        """
        TUJUAN: Verify Custom User dapat dibuat dengan email.

        AC: User creation dengan email harus berhasil
        """
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser",
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert not user.email_verified

    @pytest.mark.django_db
    def test_user_email_must_be_unique(self):
        """
        TUJUAN: Verify email field unique constraint.

        AC: Creating user dengan email sama harus raise IntegrityError
        """
        User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser1",
        )
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",
                password="testpass123",
                username="testuser2",
            )

    @pytest.mark.django_db
    def test_superuser_creation(self):
        """
        TUJUAN: Verify superuser creation dan auto email_verified.

        AC: Superuser harus memiliki is_staff=True, is_superuser=True, email_verified=True
        """
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            username="admin",
        )
        assert user.is_staff
        assert user.is_superuser
        assert user.email_verified

    @pytest.mark.django_db
    def test_user_profile_auto_created(self):
        """
        TUJUAN: Verify UserProfile auto-created via signal saat user creation.

        AC: UserProfile harus ada untuk setiap User tanpa manual create
        """
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser",
        )
        # Signal post_save di accounts/signals.py harusnya sudah buat profile
        assert UserProfile.objects.filter(user=user).exists()
        assert user.profile is not None

    @pytest.mark.django_db
    def test_user_mark_email_verified(self):
        """
        TUJUAN: Verify mark_email_verified() method works.

        AC: Setelah memanggil mark_email_verified(), email_verified harus True
        """
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser",
        )
        assert not user.email_verified

        user.mark_email_verified()
        user.refresh_from_db()

        assert user.email_verified
        assert user.email_verified_at is not None


class TestBasicViews:
    """Test basic view routing."""

    def test_admin_url_accessible(self, client):
        """
        TUJUAN: Verify admin URL dapat diakses (dan redirect ke login di dev).

        AC: Status code 200 atau 302 (redirect) OK
        """
        response = client.get("/admin/")
        assert response.status_code in [200, 302]

    def test_dashboard_url_accessible(self, client):
        """
        TUJUAN: Verify dashboard URL dapat diakses.

        AC: Dashboard index view harus accessible (200 atau redirect)
        """
        response = client.get("/dashboard/")
        assert response.status_code in [200, 302]

    def test_is_app_installed_helper(self):
        """
        TUJUAN: Verify is_app_installed helper di config.urls bekerja dengan benar.
        """
        from config.urls import is_app_installed

        assert is_app_installed("apps.core")
        assert is_app_installed("apps.accounts")
        assert is_app_installed("apps.dashboard")
        assert not is_app_installed("apps.non_existent_app")

