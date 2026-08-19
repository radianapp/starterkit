"""
Unit Tests untuk Two-Factor Authentication (TOTP / Google Authenticator).
US: US-043 — Two-Factor Authentication (2FA TOTP)
"""

import pyotp
import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from apps.accounts.models.totp import TOTPBackupCode, TOTPDevice
from apps.accounts.services.totp_service import (
    confirm_totp_device,
    disable_totp_for_user,
    generate_backup_codes,
    generate_qr_code_data_uri,
    generate_totp_secret,
    get_or_create_pending_device,
    get_totp_uri,
    is_2fa_enabled,
    user_has_2fa,
    verify_user_totp,
)

User = get_user_model()


@pytest.fixture
def user_with_2fa(db):
    """Fixture user yang sudah mengaktifkan 2FA."""
    user = User.objects.create_user(
        email="totpuser@example.com",
        username="totpuser",
        password="ValidPassword123!",
        email_verified=True,
    )
    secret = pyotp.random_base32()
    device = TOTPDevice.objects.create(
        user=user,
        secret_key=secret,
        is_confirmed=True,
    )
    generate_backup_codes(device, count=4)
    return user


@pytest.mark.django_db
class TestTOTPService:
    def test_generate_secret_and_uri(self, regular_user):
        import urllib.parse

        secret = generate_totp_secret()
        assert isinstance(secret, str)
        assert len(secret) == 32

        uri = get_totp_uri(regular_user, secret)
        assert "otpauth://totp/" in uri
        assert regular_user.email in urllib.parse.unquote(uri)
        assert secret in uri

    def test_generate_qr_code_data_uri(self):
        uri = "otpauth://totp/Test:user@example.com?secret=JBSWY3DPEHPK3PXP"
        data_uri = generate_qr_code_data_uri(uri)
        assert data_uri.startswith("data:image/png;base64,")

    def test_get_or_create_pending_device(self, regular_user):
        device, _uri, qr = get_or_create_pending_device(regular_user)
        assert device.user == regular_user
        assert not device.is_confirmed
        assert len(device.secret_key) == 32
        assert qr.startswith("data:image/png;base64,")

        # Jika dipanggil lagi saat masih pending, harus memakai device yang sama
        device2, _, _ = get_or_create_pending_device(regular_user)
        assert device.id == device2.id
        assert device.secret_key == device2.secret_key

    def test_confirm_totp_device(self, regular_user):
        device, _, _ = get_or_create_pending_device(regular_user)

        # Salah token
        success, codes = confirm_totp_device(regular_user, "000000")
        assert not success
        assert len(codes) == 0

        # Benar token
        totp = pyotp.TOTP(device.secret_key)
        valid_code = totp.now()

        success, codes = confirm_totp_device(regular_user, valid_code)
        assert success
        assert len(codes) == 8

        device.refresh_from_db()
        assert device.is_confirmed
        assert device.last_used_at is not None
        assert TOTPBackupCode.objects.filter(device=device).count() == 8

    def test_verify_user_totp_and_backup_code(self, user_with_2fa):
        device = user_with_2fa.totp_device

        # Verifikasi dengan TOTP valid
        totp = pyotp.TOTP(device.secret_key)
        valid_code = totp.now()
        assert verify_user_totp(user_with_2fa, valid_code)

        # Verifikasi dengan TOTP salah
        assert not verify_user_totp(user_with_2fa, "999999")

        # Generate backup codes baru dan simpan daftar plain text
        plain_codes = generate_backup_codes(device, count=2)
        code_1 = plain_codes[0]

        # Konsumsi code_1
        assert verify_user_totp(user_with_2fa, code_1)

        # Coba gunakan code_1 sekali lagi -> harus gagal karena sudah used
        assert not verify_user_totp(user_with_2fa, code_1)

        # Coba format tanpa tanda minus
        code_2 = plain_codes[1].replace("-", "")
        assert verify_user_totp(user_with_2fa, code_2)

    def test_disable_totp_for_user(self, user_with_2fa):
        assert user_has_2fa(user_with_2fa)
        assert disable_totp_for_user(user_with_2fa)
        assert not user_has_2fa(user_with_2fa)
        assert TOTPDevice.objects.filter(user=user_with_2fa).count() == 0


@pytest.mark.django_db
class TestTOTPViews:
    def test_setup_view_requires_login(self, client):
        url = reverse("accounts:2fa_setup")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response.url

    def test_setup_view_flow(self, client, regular_user):
        client.force_login(regular_user)
        url = reverse("accounts:2fa_setup")

        # GET setup page
        response = client.get(url)
        assert response.status_code == 200
        assert "qr_data_uri" in response.context
        assert "secret_key" in response.context

        secret_key = response.context["secret_key"]

        # POST invalid token
        response = client.post(url, {"token": "111111"})
        assert response.status_code == 422

        # POST valid token
        valid_token = pyotp.TOTP(secret_key).now()
        response = client.post(url, {"token": valid_token})
        assert response.status_code == 302
        assert response.url == reverse("accounts:2fa_backup_codes")

        # Cek backup codes page
        response = client.get(response.url)
        assert response.status_code == 200
        assert len(response.context["backup_codes"]) == 8

        # Jika diakses kedua kali tanpa session, redirect ke profile
        response2 = client.get(reverse("accounts:2fa_backup_codes"))
        assert response2.status_code == 302
        assert response2.url == reverse("accounts:profile")

    def test_disable_view(self, client, user_with_2fa):
        client.force_login(user_with_2fa)
        url = reverse("accounts:2fa_disable")

        # GET disable page
        response = client.get(url)
        assert response.status_code == 200

        # POST salah password
        response = client.post(url, {"password": "WrongPassword"})
        assert response.status_code == 422
        assert user_has_2fa(user_with_2fa)

        # POST benar password
        response = client.post(url, {"password": "ValidPassword123!"})
        assert response.status_code == 302
        assert not user_has_2fa(user_with_2fa)

    def test_login_flow_with_2fa_redirect_and_verification(self, client, user_with_2fa):
        login_url = reverse("accounts:login")

        # Step 1: Submit email & password
        response = client.post(
            login_url,
            {"identifier": user_with_2fa.email, "password": "ValidPassword123!"},
        )
        assert response.status_code == 302
        assert response.url == reverse("accounts:2fa_verify")

        # User belum terautentikasi penuh di session
        assert "_auth_user_id" not in client.session
        assert client.session.get("pre_2fa_user_id") == user_with_2fa.pk

        # Step 2: GET halaman 2FA verify
        verify_url = reverse("accounts:2fa_verify")
        response = client.get(verify_url)
        assert response.status_code == 200

        # Step 3: POST salah token
        response = client.post(verify_url, {"code": "000000"})
        assert response.status_code == 422
        assert "_auth_user_id" not in client.session

        # Step 4: POST benar token
        device = user_with_2fa.totp_device
        valid_otp = pyotp.TOTP(device.secret_key).now()

        response = client.post(verify_url, {"code": valid_otp})
        assert response.status_code == 302
        assert response.url == "/"

        # Sekarang sudah terautentikasi
        assert int(client.session["_auth_user_id"]) == user_with_2fa.pk
        assert "pre_2fa_user_id" not in client.session

    def test_login_with_backup_code(self, client, user_with_2fa):
        login_url = reverse("accounts:login")
        client.post(
            login_url,
            {"identifier": user_with_2fa.email, "password": "ValidPassword123!"},
        )

        device = user_with_2fa.totp_device
        backup_codes = generate_backup_codes(device, count=1)
        raw_code = backup_codes[0]

        verify_url = reverse("accounts:2fa_verify")
        response = client.post(verify_url, {"code": raw_code})
        assert response.status_code == 302
        assert int(client.session["_auth_user_id"]) == user_with_2fa.pk


@pytest.mark.django_db
class Test2FAToggle:
    @override_settings(ENABLE_2FA=False)
    def test_2fa_disabled_globally(self, client, user_with_2fa):
        assert not is_2fa_enabled()
        assert not user_has_2fa(user_with_2fa)

        # Login langsung masuk tanpa redirect ke 2fa_verify
        login_url = reverse("accounts:login")
        response = client.post(
            login_url,
            {"identifier": user_with_2fa.email, "password": "ValidPassword123!"},
        )
        assert response.status_code == 302
        assert response.url == "/"
        assert int(client.session["_auth_user_id"]) == user_with_2fa.pk
