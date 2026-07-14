"""
Pytest configuration dan fixtures untuk RDP Starter Kit.
US: US-017 — Test suite siap pakai

TUJUAN: Setup pytest dengan Django integration, fixtures umum, dan configuration.

ALUR:
  1. Configure pytest-django dengan DJANGO_SETTINGS_MODULE
  2. Setup fixtures untuk database, client, user, dll.
  3. Setup markers untuk test categorization
"""

import pytest
from django.test import Client

from apps.accounts.models import User


@pytest.fixture
def client():
    """
    TUJUAN: Provide Django test client untuk setiap test.

    DIPANGGIL DARI: Test functions dengan parameter `client`
    """
    return Client()


@pytest.fixture
def admin_user(db):
    """
    TUJUAN: Create superuser untuk testing admin functionality.

    ALUR:
      1. Create superuser dengan email admin@test.local
      2. Email marked as verified
      3. Return user instance

    DIPANGGIL DARI: Test functions dengan parameter `admin_user`
    """
    user = User.objects.create_superuser(
        email="admin@test.local",
        password="admin123",
        username="admin",
    )
    return user


@pytest.fixture
def regular_user(db):
    """
    TUJUAN: Create regular user untuk testing user flows.

    ALUR:
      1. Create user dengan email user@test.local
      2. Email NOT verified (normal registration flow)
      3. Return user instance

    DIPANGGIL DARI: Test functions dengan parameter `regular_user`
    """
    user = User.objects.create_user(
        email="user@test.local",
        password="user123",
        username="testuser",
    )
    return user


@pytest.fixture
def authenticated_client(client, regular_user):
    """
    TUJUAN: Provide Django test client yang sudah login.

    ALUR:
      1. Create regular user
      2. Force login via client
      3. Return client yang authenticated

    DIPANGGIL DARI: Test functions dengan parameter `authenticated_client`
    """
    client.force_login(regular_user)
    return client
