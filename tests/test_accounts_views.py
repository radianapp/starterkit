"""
Unit test untuk accounts views: login, register, profile, verify email.
US: US-004, US-005, US-006, US-008, US-009 â€” Auth flows

TUJUAN:
  Mendongkrak test coverage pada apps/accounts/views/ yang masih rendah.
  Menguji semua path utama (GET, POST valid, POST invalid, HTMX, edge cases).
"""

import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.accounts.services.email_service import generate_verification_token

# â”€â”€â”€ Fixtures â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@pytest.fixture
def client():
    """Provide Django test client."""
    return Client()


@pytest.fixture
def verified_user(db):
    """User yang sudah terverifikasi emailnya."""
    user = User.objects.create_user(
        email="verified@test.local",
        password="StrongPass123!",
        username="verifieduser",
    )
    User.objects.filter(pk=user.pk).update(email_verified=True)
    user.refresh_from_db()
    return user


@pytest.fixture
def unverified_user(db):
    """User yang belum terverifikasi emailnya."""
    user = User.objects.create_user(
        email="unverified@test.local",
        password="StrongPass123!",
        username="unverifieduser",
    )
    user.email_verified = False
    user.save()
    return user


@pytest.fixture
def auth_client(client, verified_user):
    """Client yang sudah login sebagai verified_user."""
    client.force_login(verified_user)
    return client


@pytest.fixture
def unverified_client(client, unverified_user):
    """Client yang sudah login tapi belum verifikasi email."""
    client.force_login(unverified_user)
    return client


# â”€â”€â”€ Login View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestUserLoginView:
    """Test untuk view user_login. US: US-005"""

    def test_login_get_renders_form(self, client):
        """GET /accounts/login/ harus render form login."""
        url = reverse("accounts:login")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_login_get_redirects_if_authenticated(self, auth_client):
        """GET /accounts/login/ saat sudah login harus redirect."""
        url = reverse("accounts:login")
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response["Location"] == "/"

    def test_login_post_valid_credentials(self, client, verified_user):
        """POST dengan kredensial valid harus login dan redirect."""
        url = reverse("accounts:login")
        response = client.post(url, {
            "identifier": "verified@test.local",
            "password": "StrongPass123!",
        })
        assert response.status_code == 302

    def test_login_post_invalid_credentials(self, client, db):
        """POST dengan kredensial salah harus return 422."""
        url = reverse("accounts:login")
        response = client.post(url, {
            "identifier": "nobody@test.local",
            "password": "wrongpassword",
        })
        assert response.status_code == 422

    def test_login_post_htmx_invalid_returns_fragment(self, client, db):
        """POST HTMX dengan kredensial salah harus return 422 fragment."""
        url = reverse("accounts:login")
        response = client.post(
            url,
            {"identifier": "nobody@test.local", "password": "wrong"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 422

    def test_login_post_htmx_valid_returns_hx_redirect(self, client, verified_user):
        """POST HTMX valid harus return HX-Redirect header."""
        url = reverse("accounts:login")
        response = client.post(
            url,
            {"identifier": "verified@test.local", "password": "StrongPass123!"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response

    def test_login_post_with_next_param(self, client, verified_user):
        """POST login dengan ?next harus redirect ke next URL lokal."""
        url = reverse("accounts:login") + "?next=/dashboard/"
        response = client.post(url, {
            "identifier": "verified@test.local",
            "password": "StrongPass123!",
        })
        assert response.status_code == 302
        assert response["Location"] == "/dashboard/"

    def test_login_post_external_next_is_sanitized(self, client, verified_user):
        """next URL external harus diabaikan (open redirect prevention)."""
        url = reverse("accounts:login") + "?next=http://evil.com"
        response = client.post(url, {
            "identifier": "verified@test.local",
            "password": "StrongPass123!",
        })
        assert response.status_code == 302
        assert response["Location"] == "/"


# â”€â”€â”€ Logout View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestUserLogoutView:
    """Test untuk view user_logout. US: US-006"""

    def test_logout_post_redirects(self, auth_client):
        """POST /accounts/logout/ harus logout dan redirect."""
        url = reverse("accounts:logout")
        response = auth_client.post(url)
        assert response.status_code == 302

    def test_logout_get_not_allowed(self, auth_client):
        """GET /accounts/logout/ harus return 405."""
        url = reverse("accounts:logout")
        response = auth_client.get(url)
        assert response.status_code == 405


# â”€â”€â”€ Register Wizard View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestRegisterWizardView:
    """Test untuk view register_wizard. US: US-004"""

    def test_register_get_renders_shell(self, client, db):
        """GET /accounts/register/ harus render halaman wizard."""
        url = reverse("accounts:register")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_register_step0_post_valid_email_advances(self, client, db):
        """POST step 0 dengan email valid harus advance (return 200)."""
        url = reverse("accounts:register")
        response = client.post(url, {"email": "newuser@test.local"}, HTTP_HX_REQUEST="true")
        assert response.status_code == 200

    def test_register_step0_post_invalid_email(self, client, db):
        """POST step 0 dengan email tidak valid harus return 422."""
        url = reverse("accounts:register")
        response = client.post(url, {"email": "not-an-email"}, HTTP_HX_REQUEST="true")
        assert response.status_code == 422

    def test_register_step0_post_duplicate_email(self, client, verified_user):
        """POST step 0 dengan email duplikat harus return 422."""
        url = reverse("accounts:register")
        response = client.post(url, {"email": "verified@test.local"}, HTTP_HX_REQUEST="true")
        assert response.status_code == 422

    def test_register_complete_flow_htmx(self, client, db, settings):
        """Alur register lengkap (email â†’ password) via HTMX."""
        settings.REGISTRATION_STEPS = []
        url = reverse("accounts:register")
        client.post(url, {"email": "brand_new@test.local"}, HTTP_HX_REQUEST="true")
        response = client.post(url, {
            "password1": "VeryStrongPass999!",
            "password2": "VeryStrongPass999!",
        }, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert "HX-Redirect" in response

    def test_register_complete_flow_non_htmx(self, client, db, settings):
        """Alur register non-HTMX harus redirect setelah selesai."""
        settings.REGISTRATION_STEPS = []
        url = reverse("accounts:register")
        client.post(url, {"email": "another_new@test.local"})
        response = client.post(url, {
            "password1": "VeryStrongPass999!",
            "password2": "VeryStrongPass999!",
        })
        assert response.status_code == 302

    def test_register_password_mismatch_returns_422(self, client, db, settings):
        """POST step password dengan mismatch harus return 422."""
        settings.REGISTRATION_STEPS = []
        url = reverse("accounts:register")
        client.post(url, {"email": "mismatch@test.local"}, HTTP_HX_REQUEST="true")
        response = client.post(url, {
            "password1": "VeryStrongPass999!",
            "password2": "DifferentPass999!",
        }, HTTP_HX_REQUEST="true")
        assert response.status_code == 422


# â”€â”€â”€ Profile View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestProfileView:
    """Test untuk view profile_view. US: US-009"""

    def test_profile_get_requires_login(self, client, db):
        """GET /accounts/profile/ tanpa login harus redirect ke login."""
        url = reverse("accounts:profile")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_profile_get_renders_form(self, auth_client):
        """GET /accounts/profile/ dengan login harus render form profil."""
        url = reverse("accounts:profile")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_profile_post_valid_updates_name(self, auth_client, verified_user):
        """POST form profil valid harus update nama."""
        url = reverse("accounts:profile")
        response = auth_client.post(url, {
            "first_name": "Budi",
            "last_name": "Santoso",
            "bio": "Saya developer.",
        })
        assert response.status_code == 302
        verified_user.refresh_from_db()
        assert verified_user.first_name == "Budi"

    def test_profile_post_htmx_valid_returns_fragment(self, auth_client):
        """POST HTMX valid harus return fragment dengan HX-Trigger."""
        url = reverse("accounts:profile")
        response = auth_client.post(
            url,
            {"first_name": "Andi", "last_name": "Wijaya", "bio": ""},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert "HX-Trigger" in response

    def test_profile_post_htmx_invalid_returns_422(self, auth_client):
        """POST HTMX invalid harus return 422 fragment."""
        url = reverse("accounts:profile")
        response = auth_client.post(
            url,
            {"first_name": "A" * 200, "last_name": "", "bio": ""},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 422


# â”€â”€â”€ Avatar Upload View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestAvatarUploadView:
    """Test untuk view avatar_upload_view. US: US-009"""

    def test_avatar_upload_requires_login(self, client, db):
        """POST /accounts/profile/avatar/ tanpa login harus redirect."""
        url = reverse("accounts:avatar_upload")
        response = client.post(url, {})
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_avatar_upload_get_redirects_to_profile(self, auth_client):
        """GET /accounts/profile/avatar/ harus redirect ke profile."""
        url = reverse("accounts:avatar_upload")
        response = auth_client.get(url)
        assert response.status_code == 302
        assert "profile" in response["Location"]

    def test_avatar_upload_post_no_file_returns_422(self, auth_client):
        """POST tanpa file harus return 422 (form invalid)."""
        url = reverse("accounts:avatar_upload")
        response = auth_client.post(url, {})
        assert response.status_code == 422


# â”€â”€â”€ Verify Email Views â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestVerifyEmailViews:
    """Test untuk verify email views. US: US-008"""

    def test_verify_email_valid_token(self, client, unverified_user):
        """Token valid harus mark verified dan redirect."""
        token = generate_verification_token(unverified_user)
        url = reverse("accounts:verify_email", args=[token])
        response = client.get(url)
        assert response.status_code == 302
        unverified_user.refresh_from_db()
        assert unverified_user.email_verified

    def test_verify_email_invalid_token(self, client, db):
        """Token tidak valid harus tampilkan halaman error."""
        url = reverse("accounts:verify_email", args=["invalid-token-xyz"])
        response = client.get(url)
        assert response.status_code == 200

    def test_verify_email_already_verified_is_idempotent(self, client, verified_user):
        """Token valid untuk user yang sudah verified tetap harus redirect."""
        token = generate_verification_token(verified_user)
        url = reverse("accounts:verify_email", args=[token])
        response = client.get(url)
        assert response.status_code == 302

    def test_verify_required_redirects_if_verified(self, auth_client):
        """GET verify_required saat sudah verified â†’ redirect dashboard."""
        url = reverse("accounts:verify_required")
        response = auth_client.get(url)
        assert response.status_code == 302

    def test_verify_required_renders_for_unverified(self, unverified_client):
        """GET verify_required saat belum verified â†’ render halaman."""
        url = reverse("accounts:verify_required")
        response = unverified_client.get(url)
        assert response.status_code == 200

    def test_resend_verification_already_verified(self, auth_client):
        """POST resend saat sudah verified â†’ redirect dashboard."""
        url = reverse("accounts:resend_verification")
        response = auth_client.post(url)
        assert response.status_code == 302

    def test_resend_verification_for_unverified(self, unverified_client):
        """POST resend saat belum verified â†’ kirim email dan redirect."""
        url = reverse("accounts:resend_verification")
        response = unverified_client.post(url)
        assert response.status_code == 302
