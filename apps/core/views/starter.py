"""
Views untuk halaman showcase Starter Kit — layout dan komponen Cotton.
"""

from django.views.generic import TemplateView


class StarterLayoutView(TemplateView):
    """
    Demo 4 layout Cotton bawaan Starter Kit.
    US: US-010, US-011 — Layout system
    """
    template_name = "starter/layout.html"


class StarterComponentsView(TemplateView):
    """
    Katalog semua komponen Cotton <c-rdp.*> yang tersedia di Starter Kit.
    US: US-035 — Dokumentasi komponen
    """
    template_name = "starter/components.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_items"] = [
            {"id": "tab-overview", "label": "Overview"},
            {"id": "tab-settings", "label": "Settings"},
            {"id": "tab-activity", "label": "Activity"},
        ]
        context["step_items"] = ["Upload Berkas", "Verifikasi", "Selesai"]
        context["timeline_items"] = [
            {"title": "Akun dibuat", "desc": "User mendaftar via form register", "time": "2 jam lalu"},
            {"title": "Email diverifikasi", "desc": "Link verifikasi diklik", "time": "1 jam lalu"},
            {"title": "Login pertama", "desc": "Masuk ke dashboard", "time": "30 menit lalu"},
        ]
        return context
