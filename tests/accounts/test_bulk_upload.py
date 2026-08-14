import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.accounts.services.user_service import process_bulk_users

User = get_user_model()


@pytest.fixture
def superadmin_user():
    return User.objects.create_superuser("admin@test.com", "pass123", username="admin")


@pytest.fixture
def normal_user():
    return User.objects.create_user("user@test.com", "pass123", username="user")


@pytest.mark.django_db
def test_process_bulk_users():
    """Test service process_bulk_users."""
    rows = [
        {"email": "bulk1@test.com", "first_name": "Satu", "department": "IT"},
        {"email": "bulk2@test.com", "last_name": "Dua", "department": "HR"},
        {"email": "bulk1@test.com", "first_name": "Tiga"},  # duplicate email
    ]

    results = process_bulk_users(rows)

    assert results["success"] == 2
    assert results["failed"] == 1

    u1 = User.objects.get(email="bulk1@test.com")
    assert u1.first_name == "Satu"
    assert u1.profile.extra_data["department"] == "IT"
    assert u1.profile.extra_data["must_change_password"] is True


@pytest.mark.django_db
def test_bulk_upload_view_access(client, superadmin_user, normal_user):
    """Test akses view bulk upload."""
    url = reverse("accounts:user_bulk_upload")

    # Anonymous redirect
    response = client.get(url)
    assert response.status_code == 302

    # Normal user forbidden
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403

    # Superadmin success
    client.force_login(superadmin_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_force_password_change_middleware(client):
    """Test middleware force password change."""
    user = User.objects.create_user("test@test.com", "pass123", username="test_force")
    user.profile.extra_data = {"must_change_password": True}
    user.profile.save()

    client.force_login(user)

    # Akses dashboard harus di-redirect ke force_password_change
    response = client.get(reverse("dashboard:index"))
    assert response.status_code == 302
    assert response.url == reverse("accounts:force_password_change")

    # Akses force_password_change diperbolehkan
    response = client.get(reverse("accounts:force_password_change"))
    assert response.status_code == 200
