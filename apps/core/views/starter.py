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


class StarterCliView(TemplateView):
    """
    Dokumentasi RDP CLI — daftar perintah, grup fungsi, contoh penggunaan.
    US: US-024 — CLI rdp
    """
    template_name = "starter/cli.html"
