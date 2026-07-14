"""
Views untuk halaman publik landing page RDP-UI Framework.
US: US-038 — Halaman Landing RDP-UI Framework (Extras)
"""

from django.views.generic import TemplateView


class RdpUiLandingView(TemplateView):
    """
    Menampilkan halaman promosi dan playground interaktif untuk RDP-UI Framework.
    """

    template_name = "public/rdp_ui_landing.html"
