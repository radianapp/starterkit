from django.http import HttpResponse
from django.template.loader import render_to_string
from django.test import Client, SimpleTestCase
from django.urls import reverse

from apps.core.utils.htmx import htmx_redirect, htmx_refresh, htmx_trigger, is_htmx


class TestExtras(SimpleTestCase):
    """
    Unit test untuk fitur RDP UI Framework extras (Tema, Komponen baru, HTMX helpers).
    """

    def render_comp(self, context_dict):
        """Helper untuk me-render component menggunakan file test_components_render.html."""
        return render_to_string("test_components_render.html", context_dict)

    # 1. Test Komponen Rating
    def test_rating_rendering(self):
        html = self.render_comp(
            {
                "test_comp": "rating",
                "value": "3",
                "max": "5",
                "name": "my_rating",
                "readonly": "false",
            }
        )
        assert "rdp-rating" in html
        assert "maxStars: parseInt('5')" in html
        assert "currentValue: parseInt('3')" in html

    # 2. Test Komponen Timeline
    def test_timeline_rendering(self):
        html = self.render_comp(
            {
                "test_comp": "timeline",
                "title": "Registrasi",
                "time": "10:00",
                "icon": "👤",
                "variant": "success",
                "content": "User berhasil mendaftar.",
            }
        )
        assert "rdp-timeline" in html
        assert "rdp-timeline-item--success" in html
        assert "Registrasi" in html
        assert "10:00" in html
        assert "User berhasil mendaftar." in html

    # 3. Test Komponen Theme Picker
    def test_theme_picker_rendering(self):
        html = self.render_comp({"test_comp": "theme_picker"})
        assert "rdp-theme-picker" in html
        assert "Mode Tema" in html
        assert "Warna Aksen" in html

    # 4. Test View Landing Page RDP-UI
    # /rdp-ui/ redirect ke ui.radian.web.id (external).
    def test_landing_page_view(self):
        client = Client()
        response = client.get(reverse("rdp-ui-landing"))
        assert response.status_code == 302
        assert response["Location"] == "https://ui.radian.web.id"

    def test_home_page_has_rdp_ui_content(self):
        """Home page (/) sekarang memuat konten landing RDP UI."""
        client = Client()
        response = client.get(reverse("home"), follow=True)
        assert response.status_code == 200
        assert b"RDP UI" in response.content

    # 5. Test HTMX Helpers
    def test_is_htmx(self):
        class MockRequest:
            def __init__(self, headers):
                self.headers = headers

        request_with_htmx = MockRequest({"HX-Request": "true"})
        request_without_htmx = MockRequest({"HX-Request": "false"})
        request_none = MockRequest({})

        assert is_htmx(request_with_htmx) is True
        assert is_htmx(request_without_htmx) is False
        assert is_htmx(request_none) is False

    def test_htmx_redirect(self):
        response = htmx_redirect("/target-url/")
        assert response.status_code == 200
        assert response["HX-Redirect"] == "/target-url/"

    def test_htmx_refresh(self):
        response = htmx_refresh()
        assert response.status_code == 200
        assert response["HX-Refresh"] == "true"

    def test_htmx_trigger(self):
        response = HttpResponse("Halo")
        response = htmx_trigger(response, "show-toast", {"message": "Hello"})
        assert response["HX-Trigger"] == '{"show-toast": {"message": "Hello"}}'


class TestRdpUiTokenTestView(SimpleTestCase):
    """
    /rdp-ui/tokens/ sekarang redirect ke ui.radian.web.id/docs/ (endpoint dihapus).
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("rdp_ui_token_test")

    def test_token_test_redirects_to_external(self):
        """Verify /rdp-ui/tokens/ redirect ke ui.radian.web.id/docs/."""
        response = self.client.get(self.url)
        assert response.status_code == 302
        assert response["Location"] == "https://ui.radian.web.id/docs/"
