"""
Views untuk halaman demo komponen internal RDP-UI.
US: US-035 — Halaman demo komponen internal /dev/components/
"""

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView


class DevComponentsView(TemplateView):
    """
    Menampilkan semua varian komponen RDP-UI untuk tujuan dokumentasi internal dan testing.
    Hanya aktif jika DEBUG=True.
    """

    template_name = "dev_components.html"

    def dispatch(self, request, *args, **kwargs):
        if not settings.DEBUG:
            raise Http404("Halaman tidak ditemukan.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Data dummy untuk demonstrasi komponen
        context["tab_items"] = [
            {"id": "tab1", "label": "Informasi"},
            {"id": "tab2", "label": "Pengaturan"},
            {"id": "tab3", "label": "Keamanan"},
        ]
        context["step_items"] = ["Unggah Berkas", "Verifikasi Data", "Selesai"]
        return context
