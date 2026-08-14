"""
Views untuk halaman pengaturan (Settings).

TUJUAN: Handle GET/POST pengaturan sistem dan preferensi pengguna.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from apps.accounts.services.settings_service import update_user_preferences


class SettingsView(LoginRequiredMixin, View):
    """
    TUJUAN: Tampilkan dan simpan pengaturan global aplikasi (profil, tema, dsb).
    """

    template_name = "accounts/settings.html"

    def get(self, request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        extra_data = profile.extra_data if profile else {}

        # Ambil nilai default atau current
        current_theme = extra_data.get("theme", "system")
        current_rows = extra_data.get("rows_per_page", 20)

        return render(
            request,
            self.template_name,
            {
                "page_title": "Pengaturan",
                "current_theme": current_theme,
                "current_rows": current_rows,
            },
        )

    def post(self, request, *args, **kwargs):
        # Tangkap data dari form HTMX
        theme = request.POST.get("theme")
        rows = request.POST.get("rows_per_page")

        data_to_update = {}
        if theme:
            data_to_update["theme"] = theme
        if rows:
            try:
                data_to_update["rows_per_page"] = int(rows)
            except ValueError:
                pass

        # Simpan via service
        update_user_preferences(request.user, data_to_update)

        # Return success toast
        messages.success(request, "Pengaturan sistem berhasil disimpan.")

        if request.headers.get("HX-Request"):
            response = HttpResponse("")
            response["HX-Refresh"] = (
                "true"  # Refresh agar tema/UI beradaptasi jika ada class global
            )
            return response

        return self.get(request)
