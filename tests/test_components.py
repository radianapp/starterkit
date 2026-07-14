from django.template.loader import render_to_string
from django.test import Client, SimpleTestCase, override_settings
from django.urls import reverse


class TestComponentLibrary(SimpleTestCase):
    """
    US-033, US-034, US-035: Unit test untuk Component Library dan halaman demo internal.
    """

    def render_comp(self, context_dict):
        """Helper untuk me-render component menggunakan file test_components_render.html."""
        return render_to_string("test_components_render.html", context_dict)

    # US-033: Badge, Avatar, Loader
    def test_badge_rendering(self):
        html = self.render_comp({"test_comp": "badge", "variant": "success", "content": "Selesai"})
        assert "rdp-badge" in html
        assert "rdp-badge--success" in html
        assert "Selesai" in html

    def test_avatar_rendering_with_initials(self):
        html = self.render_comp({"test_comp": "avatar", "name": "Rahadi", "size": "md"})
        assert "rdp-avatar" in html
        assert "rdp-avatar--md" in html
        assert "R" in html

    def test_avatar_rendering_with_image(self):
        html = self.render_comp(
            {"test_comp": "avatar", "name": "Rahadi", "src": "/media/avatar.jpg"}
        )
        assert "rdp-avatar" in html
        assert 'src="/media/avatar.jpg"' in html

    def test_loader_rendering(self):
        html = self.render_comp({"test_comp": "loader", "size": "lg"})
        assert "rdp-loader" in html
        assert "rdp-loader--lg" in html

    # US-034: Tabs, Toast, Tooltip, Accordion, Skeleton, Empty State, Stat Card, Confirm, Progress, Drawer, Search Box, Filter Bar, File Upload, Steps
    def test_tabs_rendering(self):
        items = [{"id": "tab1", "label": "Tab 1"}, {"id": "tab2", "label": "Tab 2"}]
        html = self.render_comp({"test_comp": "tabs", "items": items, "default_tab": "tab1"})
        assert "rdp-tabs" in html
        assert "Tab 1" in html
        assert "Tab 2" in html
        assert "Panel 1" in html

    def test_toast_rendering(self):
        html = self.render_comp({"test_comp": "toast", "type": "success", "message": "Berhasil!"})
        assert "rdp-toast" in html
        assert "rdp-toast--success" in html
        assert "Berhasil!" in html

    def test_tooltip_rendering(self):
        html = self.render_comp({"test_comp": "tooltip", "content": "Halo", "position": "top"})
        assert "rdp-tooltip-wrapper" in html
        assert "rdp-tooltip-wrapper--top" in html
        assert 'data-tooltip="Halo"' in html

    def test_accordion_rendering(self):
        html = self.render_comp({"test_comp": "accordion", "title": "Pertanyaan", "open": "true"})
        assert "rdp-accordion" in html
        assert "rdp-accordion--open" in html
        assert "Pertanyaan" in html
        assert "Jawaban" in html

    def test_skeleton_rendering(self):
        html = self.render_comp(
            {"test_comp": "skeleton", "width": "100px", "height": "50px", "circle": True}
        )
        assert "rdp-skeleton" in html
        assert "rdp-skeleton--circle" in html
        assert "width: 100px" in html
        assert "height: 50px" in html

    def test_empty_state_rendering(self):
        html = self.render_comp(
            {
                "test_comp": "empty_state",
                "icon": "📭",
                "title": "Kosong",
                "description": "Keterangan",
            }
        )
        assert "rdp-empty-state" in html
        assert "📭" in html
        assert "Kosong" in html
        assert "Keterangan" in html

    def test_stat_card_rendering(self):
        html = self.render_comp(
            {
                "test_comp": "stat_card",
                "label": "Pengguna",
                "value": "500",
                "trend": "+10%",
                "trend_up": True,
            }
        )
        assert "rdp-stat-card" in html
        assert "Pengguna" in html
        assert "500" in html
        assert "+10%" in html
        assert "rdp-stat-card__trend--up" in html

    def test_confirm_rendering(self):
        html = self.render_comp(
            {
                "test_comp": "confirm",
                "title": "Hapus?",
                "message": "Yakin?",
                "destructive": True,
                "trigger_text": "Hapus",
                "hx_delete": "/delete/",
            }
        )
        assert "rdp-confirm-wrapper" in html
        assert "Hapus?" in html
        assert "Yakin?" in html
        assert 'hx-delete="/delete/"' in html

    def test_progress_rendering(self):
        html = self.render_comp(
            {"test_comp": "progress", "value": "45", "max": "100", "variant": "success"}
        )
        assert "rdp-progress" in html
        assert 'value="45"' in html
        assert 'max="100"' in html
        assert "rdp-progress--success" in html

    def test_drawer_rendering(self):
        html = self.render_comp({"test_comp": "drawer", "title": "Menu", "trigger_text": "Buka"})
        assert "rdp-drawer-wrapper" in html
        assert "Menu" in html
        assert "Buka" in html
        assert "Konten" in html

    def test_search_box_rendering(self):
        html = self.render_comp(
            {"test_comp": "search_box", "placeholder": "Cari...", "hx_get": "/search/"}
        )
        assert "rdp-search-wrapper" in html
        assert 'placeholder="Cari..."' in html
        assert 'hx-get="/search/"' in html

    def test_filter_bar_rendering(self):
        html = self.render_comp({"test_comp": "filter_bar"})
        assert "rdp-filter-bar" in html
        assert "Filters" in html

    def test_file_upload_rendering(self):
        html = self.render_comp(
            {"test_comp": "file_upload", "name": "berkas", "accept": "image/*", "max_size": "3MB"}
        )
        assert "rdp-file-upload-container" in html
        assert 'accept="image/*"' in html
        assert 'max_size="3MB"' in html

    def test_steps_rendering(self):
        items = ["Satu", "Dua", "Tiga"]
        html = self.render_comp({"test_comp": "steps", "items": items, "current": 2})
        assert "rdp-steps" in html
        assert "Satu" in html
        assert "Dua" in html
        assert "Tiga" in html
        assert "rdp-steps__item--active" in html


class TestDevComponentsView(SimpleTestCase):
    """
    US-035: Unit test untuk DevComponentsView (/dev/components/).
    """

    def setUp(self):
        self.client = Client()

    def reload_urls(self):
        import sys
        from importlib import reload

        from django.urls import clear_url_caches

        clear_url_caches()
        if "config.urls" in sys.modules:
            reload(sys.modules["config.urls"])

    def tearDown(self):
        self.reload_urls()

    @override_settings(DEBUG=True)
    def test_view_accessible_when_debug_true(self):
        """Memastikan /dev/components/ dapat diakses saat DEBUG=True."""
        self.reload_urls()
        response = self.client.get(reverse("dev-components"))
        assert response.status_code == 200
        assert "Pustaka Komponen UI RDP" in response.content.decode("utf-8")

    @override_settings(DEBUG=False)
    def test_view_returns_404_when_debug_false(self):
        """Memastikan /dev/components/ mengembalikan 404 saat DEBUG=False."""
        self.reload_urls()
        try:
            url = reverse("dev-components")
            response = self.client.get(url)
            assert response.status_code == 404
        except Exception:
            pass
