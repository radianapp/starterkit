"""
Unit test untuk htmx_examples.py
US: US-036 — 10 HTMX patterns
"""
import json

import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    return Client()

class TestHtmxExamplesViews:
    def test_index_view(self, client):
        url = reverse("htmx-examples")
        response = client.get(url)
        assert response.status_code == 200
        assert "contacts" in response.context

    def test_contact_create_view_get(self, client):
        url = reverse("htmx-contact-create")
        response = client.get(url)
        assert response.status_code == 200

    def test_contact_create_view_post_valid_htmx(self, client):
        url = reverse("htmx-contact-create")
        response = client.post(
            url,
            {"name": "Test User", "email": "test@radian.web.id", "phone": "08123"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response
        assert "HX-Trigger" in response
        trigger_data = json.loads(response["HX-Trigger"])
        assert "showToast" in trigger_data

    def test_contact_create_view_post_valid_non_htmx(self, client):
        url = reverse("htmx-contact-create")
        response = client.post(
            url,
            {"name": "Test User 2", "email": "test2@radian.web.id", "phone": "08124"},
        )
        assert response.status_code == 302

    def test_contact_create_view_post_invalid(self, client):
        url = reverse("htmx-contact-create")
        response = client.post(
            url,
            {"name": "Spammer", "email": "bad@spam.test", "phone": "08124"},
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 422

    def test_contact_delete_view(self, client):
        url = reverse("htmx-contact-delete", args=[1])
        response = client.delete(url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert response.content == b""
        trigger_data = json.loads(response["HX-Trigger"])
        assert trigger_data["showToast"]["type"] == "success"

    def test_live_validation_view(self, client):
        url = reverse("htmx-live-validation")
        resp = client.post(url, {"email": ""})
        assert b"Email tidak boleh kosong" in resp.content
        resp = client.post(url, {"email": "invalid"})
        assert b"Format email tidak valid" in resp.content
        resp = client.post(url, {"email": "bad@spam.test"})
        assert b"dilarang" in resp.content
        resp = client.post(url, {"email": "new_email@radian.web.id"})
        assert b"Email tersedia!" in resp.content

    def test_inline_edit_view_get_existing(self, client):
        url = reverse("htmx-contact-edit", args=[2])
        response = client.get(url)
        assert response.status_code == 200

    def test_inline_edit_view_get_not_found(self, client):
        url = reverse("htmx-contact-edit", args=[999])
        response = client.get(url)
        assert response.status_code == 404

    def test_inline_edit_view_post_valid(self, client):
        url = reverse("htmx-contact-edit", args=[2])
        response = client.post(url, {
            "name": "Rahadi Updated",
            "email": "rahadi.up@radian.web.id",
            "phone": "123"
        })
        assert response.status_code == 200

    def test_inline_edit_view_post_invalid(self, client):
        url = reverse("htmx-contact-edit", args=[2])
        response = client.post(url, {"name": "", "email": ""})
        assert response.status_code == 400

    def test_inline_edit_view_post_not_found(self, client):
        url = reverse("htmx-contact-edit", args=[999])
        response = client.post(url, {"name": "X", "email": "x@x.com"})
        assert response.status_code == 404

    def test_search_view_empty_query(self, client):
        url = reverse("htmx-contact-search")
        response = client.get(url)
        assert response.status_code == 200

    def test_search_view_with_query(self, client):
        url = reverse("htmx-contact-search")
        response = client.get(url, {"q": "Ani"})
        assert response.status_code == 200

    def test_infinite_scroll_view(self, client):
        url = reverse("htmx-infinite-scroll")
        response = client.get(url)
        assert response.status_code == 200
        assert "initial_rows" in response.context

    def test_infinite_scroll_rows_view_page_1(self, client):
        url = reverse("htmx-infinite-scroll-rows")
        response = client.get(url, {"page": "1"})
        assert response.status_code == 200

    def test_job_status_polling_view(self, client):
        url = reverse("htmx-polling")
        resp1 = client.get(url, {"action": "start"})
        assert resp1.status_code == 200
        resp2 = client.get(url)
        assert resp2.status_code == 200

    def test_toast_demo_view(self, client):
        url = reverse("htmx-toast-demo")
        response = client.post(url, {"type": "info", "message": "Halo!"})
        assert response.status_code == 200
        assert "HX-Trigger" in response
