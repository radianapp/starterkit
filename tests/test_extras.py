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
    # /rdp-ui/ sekarang redirect ke / karena landing sudah disatukan.
    def test_landing_page_view(self):
        client = Client()
        # /rdp-ui/ harus redirect 302 ke /
        response = client.get(reverse("rdp-ui-landing"))
        assert response.status_code == 302
        assert response["Location"] == "/"

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
    Unit test untuk halaman Token Test RDP UI (/rdp-ui/tokens/).
    Memverifikasi bahwa semua 11 tema dan token tampil dengan benar.
    """

    def setUp(self):
        """Setup client dan URL untuk semua test."""
        self.client = Client()
        self.url = reverse("rdp_ui_token_test")

    def test_token_test_page_accessible(self):
        """Verify halaman /rdp-ui/tokens/ dapat diakses tanpa login dan mengembalikan 200."""
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_token_test_uses_correct_template(self):
        """Verify halaman menggunakan template rdp_ui/token_test.html."""
        response = self.client.get(self.url)
        assert "rdp_ui/token_test.html" in [t.name for t in response.templates]

    def test_token_test_context_has_themes(self):
        """Verify context mengandung daftar 11 tema dengan field yang benar."""
        response = self.client.get(self.url)
        themes = response.context["themes"]
        assert len(themes) == 11
        for theme in themes:
            assert "id" in theme
            assert "label" in theme
            assert "swatch" in theme
            assert "dark" in theme

    def test_token_test_context_theme_count(self):
        """Verify context theme_count sesuai dengan panjang daftar themes."""
        response = self.client.get(self.url)
        assert response.context["theme_count"] == 11
        assert response.context["theme_count"] == len(response.context["themes"])

    def test_token_test_all_theme_ids_in_html(self):
        """
        Verify semua ID tema hadir di HTML sebagai data-rdp-theme di card gallery.
        Ini memastikan Theme Gallery merender card untuk setiap tema.
        """
        response = self.client.get(self.url)
        html = response.content.decode("utf-8")
        expected_ids = [
            "default", "light", "corporate", "ocean", "forest",
            "github", "dark", "midnight", "nord", "dracula", "terminal",
        ]
        for theme_id in expected_ids:
            assert f'data-theme-id="{theme_id}"' in html, (
                f"Theme card untuk '{theme_id}' tidak ditemukan di HTML gallery"
            )

    def test_token_test_all_theme_css_links_in_html(self):
        """
        Verify semua 11 file CSS tema di-load bersamaan di <head>.
        Ini penting agar Theme Gallery dapat merender setiap card dengan warna yang benar.
        """
        response = self.client.get(self.url)
        html = response.content.decode("utf-8")
        expected_ids = [
            "default", "light", "corporate", "ocean", "forest",
            "github", "dark", "midnight", "nord", "dracula", "terminal",
        ]
        for theme_id in expected_ids:
            assert f"{theme_id}.css" in html, (
                f"File CSS tema '{theme_id}.css' tidak ditemukan di <head> halaman"
            )
