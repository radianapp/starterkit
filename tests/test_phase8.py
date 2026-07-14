"""
Unit tests untuk Phase 8 - Public Pages & HTMX Patterns.
US: US-029, US-030, US-031, US-032, US-036
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from django.views.generic import FormView

from apps.core.mixins.htmx import HtmxFormMixin
from apps.core.views.htmx_examples import ContactForm
from apps.dashboard.models.activity import Activity

User = get_user_model()


# Simple View untuk menguji HtmxFormMixin
class DummyFormView(HtmxFormMixin, FormView):
    form_class = ContactForm
    template_name = "htmx_examples/partials/contact_form.html"
    success_url = "/success/"


@pytest.mark.django_db
class TestPhase8HTMXAndPublicPages:
    """Test Suite untuk memverifikasi fungsionalitas Phase 8."""

    def test_htmx_form_mixin_invalid_htmx(self):
        """Verify HtmxFormMixin mengembalikan status 422 untuk request HTMX yang tidak valid."""
        rf = RequestFactory()
        # Request dikirim via POST dengan data kosong (invalid) dan header HX-Request
        request = rf.post("/dummy-url/", data={}, HTTP_HX_REQUEST="true")

        view = DummyFormView()
        view.setup(request)

        form = ContactForm(data={})
        assert not form.is_valid()

        response = view.form_invalid(form)
        assert response.status_code == 422

    def test_htmx_form_mixin_valid_htmx(self):
        """Verify HtmxFormMixin mengembalikan HX-Redirect untuk request HTMX yang valid."""
        rf = RequestFactory()
        valid_data = {"name": "Budi Santoso", "email": "budi@example.com", "phone": "0812345"}
        request = rf.post("/dummy-url/", data=valid_data, HTTP_HX_REQUEST="true")

        view = DummyFormView()
        view.setup(request)

        form = ContactForm(data=valid_data)
        assert form.is_valid()

        response = view.form_valid(form)
        assert response.status_code == 200
        assert response.has_header("HX-Redirect")
        assert response["HX-Redirect"] == "/success/"

    def test_public_pages_accessible(self, client):
        """Verify halaman publik dapat diakses tanpa login dan menggunakan template yang benar."""
        urls = [
            ("home", 200),
            ("about", 200),
            ("terms", 200),
            ("privacy", 200),
        ]
        for name, expected_status in urls:
            response = client.get(reverse(name))
            assert response.status_code == expected_status

    def test_dashboard_authenticated(self, client):
        """Verify halaman dashboard tidak dapat diakses tanpa login (redirect ke login)."""
        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 302
        assert "login" in response.url

    def test_dashboard_with_demo_data(self, client):
        """Verify dashboard index mengembalikan data KPI dan pagination aktivitas setelah login."""
        # Buat user dan login
        user = User.objects.create_user(
            username="testuser@rdp.test", email="testuser@rdp.test", password="password123"
        )
        client.login(username="testuser@rdp.test", password="password123")

        # Buat dummy aktivitas
        Activity.objects.create(
            user=user, title="Aktivitas Test 1", status="completed", amount=50000.00
        )
        Activity.objects.create(user=user, title="Aktivitas Test 2", status="pending", amount=0.00)

        response = client.get(reverse("dashboard:index"))
        assert response.status_code == 200
        assert response.context["total_users"] >= 1
        assert response.context["total_activities"] == 2
        assert float(response.context["total_revenue"]) == 50000.00
        assert response.context["pending_activities"] == 1
        assert len(response.context["page_obj"]) == 2

    def test_htmx_showcase_endpoints(self, client):
        """Verify endpoint showcase HTMX dapat diakses."""
        # Login agar diizinkan masuk
        User.objects.create_user(
            username="tester@rdp.test", email="tester@rdp.test", password="password123"
        )
        client.login(username="tester@rdp.test", password="password123")

        response = client.get(reverse("htmx-examples"))
        assert response.status_code == 200

        # Test live validation endpoint
        response = client.post(reverse("htmx-live-validation"), data={"email": "test@spam.test"})
        assert response.status_code == 200
        assert "dilarang" in response.content.decode("utf-8")

        # Test polling endpoint
        response = client.get(reverse("htmx-polling"))
        assert response.status_code == 200
