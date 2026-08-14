"""
Unit Tests untuk Observability Dashboard, HealthCheck Probe, dan Security Auditor Command
"""

import io

import pytest
from django.core.management import call_command

from apps.accounts.models import User


@pytest.mark.django_db
def test_healthcheck_endpoint(client):
    """Memastikan endpoint /healthz/ mengembalikan JSON status 200 OK."""
    response = client.get("/healthz/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["checks"]["database"] == "ok"


@pytest.mark.django_db
def test_telemetry_dashboard_permission_denied_for_normal_user(client):
    """Memastikan user biasa/anonim mendapatkan status 403 Forbidden saat mengakses /dev/telemetry/."""
    normal_user = User.objects.create_user(
        username="normaluser", email="normaluser@example.com", password="password"
    )
    client.force_login(normal_user)

    response = client.get("/dev/telemetry/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_telemetry_dashboard_allowed_for_superuser(client):
    """Memastikan superuser dapat mengakses /dev/telemetry/ dengan status 200 OK."""
    superuser = User.objects.create_superuser(
        username="adminuser", email="admin@example.com", password="password"
    )
    client.force_login(superuser)

    response = client.get("/dev/telemetry/")
    assert response.status_code == 200
    assert "Observability & Telemetry Dashboard" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_audit_security_command():
    """Memastikan command audit_security berjalan sukses."""
    out = io.StringIO()
    call_command("audit_security", stdout=out)
    output = out.getvalue()

    assert "Security & Compliance Audit Report" in output
    assert "SECRET_KEY" in output
    assert "DEBUG Mode" in output
