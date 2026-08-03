from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase, override_settings


class TestLayouts(SimpleTestCase):
    """
    US-026, US-027, US-028: Unit test untuk sistem Layout (c-layout.*)
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = AnonymousUser()

    def render_layout(self, layout_name, context_dict=None):
        """Helper to render a cotton layout with a request context."""
        context_data = {
            "request": self.request,
            "test_layout": layout_name,
            "SITE_NAME": "RDP Starter Kit",
            "COMPANY_NAME": "Radian Data Platform",
            "APP_BRAND_SHORT": "RDP",
            "COPYRIGHT_YEAR": "2026",
            "RDP_UI_VERSION": "v1.0",
            "RDP_UI_SELF_HOST": False,
        }
        if context_dict:
            context_data.update(context_dict)

        return render_to_string("test_layouts_render.html", context_data, request=self.request)

    @override_settings(RDP_UI_SELF_HOST=False, RDP_UI_VERSION="v1.0")
    def test_cdn_assets_loaded_when_self_host_false(self):
        """Memastikan aset diload dari CDN ketika RDP_UI_SELF_HOST=False."""
        html = self.render_layout("base", {"RDP_UI_SELF_HOST": False, "RDP_UI_VERSION": "v1.0"})
        assert "https://ui.radian.web.id/v1.0/assets/rdp.css" in html
        assert "https://cdn.jsdelivr.net/npm/@picocss/pico" in html
        assert "https://unpkg.com/htmx.org" in html
        assert "static/css/layout.css" in html

    @override_settings(RDP_UI_SELF_HOST=True)
    def test_self_hosted_assets_loaded_when_self_host_true(self):
        """Memastikan aset diload dari folder static lokal ketika RDP_UI_SELF_HOST=True."""
        html = self.render_layout("base", {"RDP_UI_SELF_HOST": True})
        assert "static/vendor/rdp-ui/rdp.css" in html
        assert "static/vendor/picocss/pico.min.css" in html
        assert "static/vendor/htmx/htmx.min.js" in html

    def test_all_seven_layouts_render(self):
        """Memastikan ketujuh layout Cotton dapat dirender tanpa error."""
        layouts = ["base", "auth", "public", "app", "error", "email", "print"]
        for layout in layouts:
            html = self.render_layout(layout)
            assert "Hello World" in html or "SITE_NAME" in html

    def test_layout_accessibility_skip_link(self):
        """Memastikan link skip-nav untuk aksesibilitas ada di base layout."""
        html = self.render_layout("base")
        assert 'class="rdp-skip-link"' in html
        assert 'href="#main-content"' in html

    @override_settings(DEBUG=True)
    def test_layout_debug_overlay_gate(self):
        """Memastikan panel debug overlay hanya muncul jika DEBUG=True."""
        html_with = self.render_layout("base", {"DEBUG": True})
        assert "rdp-debug-overlay" in html_with

    @override_settings(DEBUG=False)
    def test_layout_debug_overlay_hidden_when_debug_false(self):
        """Memastikan panel debug overlay tidak muncul jika DEBUG=False."""
        html_without = self.render_layout("base", {"DEBUG": False})
        assert "rdp-debug-overlay" not in html_without
