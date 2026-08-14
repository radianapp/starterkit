"""
Views untuk halaman Docs dan Examples Starter Kit.
"""

from django.views.generic import TemplateView


class StarterDocsView(TemplateView):
    """
    Dokumentasi lengkap RDP Starter Kit — instalasi, layout, komponen, auth, CLI, deploy.
    US: US-010, US-024, US-035
    """

    template_name = "starter/docs.html"


class StarterExamplesView(TemplateView):
    """
    Index semua contoh dan demo interaktif Starter Kit.
    US: US-036
    """

    template_name = "starter/examples.html"


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
