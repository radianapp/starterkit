"""
Unit Tests untuk Multi-Tenancy & Tenant Switcher (US-027)
"""

import pytest
from django.test import override_settings

from apps.accounts.models import User
from apps.tenants.middleware import TenantMiddleware
from apps.tenants.models import Organization, OrganizationMember
from apps.tenants.services import switch_active_tenant


@pytest.mark.django_db
def test_organization_model_creation():
    """Memastikan pembuatan Organization dan OrganizationMember berjalan dengan benar."""
    user = User.objects.create_user(
        username="owner", email="owner@example.com", password="password"
    )
    org = Organization.objects.create(name="Acme Corp", owner=user)

    assert org.slug == "acme-corp"
    assert str(org) == "Acme Corp (acme-corp)"

    member = OrganizationMember.objects.create(organization=org, user=user, role="owner")
    assert member.role == "owner"


@pytest.mark.django_db
@override_settings(RDP_MULTI_TENANCY_ENABLED=False)
def test_tenant_middleware_disabled(rf):
    """Memastikan TenantMiddleware di-bypass saat RDP_MULTI_TENANCY_ENABLED=False."""
    request = rf.get("/")
    middleware = TenantMiddleware(lambda req: None)
    middleware(request)

    assert request.is_multi_tenancy_enabled is False
    assert request.tenant is None


@pytest.mark.django_db
@override_settings(RDP_MULTI_TENANCY_ENABLED=True)
def test_tenant_middleware_enabled(rf):
    """Memastikan TenantMiddleware menginjeksi request.tenant saat RDP_MULTI_TENANCY_ENABLED=True."""
    user = User.objects.create_user(username="member1", email="m1@example.com", password="password")
    org = Organization.objects.create(name="Stark Industries", owner=user)
    OrganizationMember.objects.create(organization=org, user=user, role="owner")

    request = rf.get("/")
    request.user = user
    request.session = {}

    middleware = TenantMiddleware(lambda req: None)
    middleware(request)

    assert request.is_multi_tenancy_enabled is True
    assert request.tenant == org


@pytest.mark.django_db
def test_switch_tenant_service(rf):
    """Memastikan service switch_active_tenant mengupdate session ID tenant aktif."""
    user = User.objects.create_user(username="member2", email="m2@example.com", password="password")
    org = Organization.objects.create(name="Wayne Enterprises", owner=user)
    OrganizationMember.objects.create(organization=org, user=user, role="owner")

    request = rf.get("/")
    request.user = user
    request.session = {}

    success = switch_active_tenant(request, org.id)
    assert success is True
    assert request.session.get("active_tenant_id") == org.id
