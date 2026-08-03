import pytest
from django.urls import reverse
from apps.accounts.models.passkey import PasskeyCredential


@pytest.mark.django_db
class TestWebAuthnRoutes:
    def test_login_challenge_route(self, client):
        url = reverse("accounts:webauthn_login_challenge")
        # Should be POST only
        response = client.get(url)
        assert response.status_code == 405
        
        response = client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert "challenge" in data
        assert "rpId" in data

    def test_register_challenge_requires_login(self, client):
        url = reverse("accounts:webauthn_register_challenge")
        response = client.post(url)
        # Should redirect to login
        assert response.status_code == 302
        assert "login" in response.url

    def test_register_challenge_logged_in(self, client, regular_user):
        client.force_login(regular_user)
        url = reverse("accounts:webauthn_register_challenge")
        response = client.post(url)
        assert response.status_code == 200
        data = response.json()
        assert "challenge" in data
        assert "user" in data
        assert data["user"]["name"] == regular_user.email

    def test_delete_passkey(self, client, regular_user):
        client.force_login(regular_user)
        passkey = PasskeyCredential.objects.create(
            user=regular_user,
            name="My Device",
            credential_id="base64urlid",
            public_key="base64urlpk",
            sign_count=0
        )
        assert PasskeyCredential.objects.count() == 1
        
        url = reverse("accounts:webauthn_delete_passkey", args=[passkey.id])
        response = client.delete(url)
        assert response.status_code == 200
        assert response.headers.get("HX-Trigger") == "passkeyDeleted"
        assert PasskeyCredential.objects.count() == 0
