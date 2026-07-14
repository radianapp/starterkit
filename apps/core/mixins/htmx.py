"""
Mixin untuk penanganan form via HTMX.
US: US-029 — HTMX form validation pattern — 422 fragment + HX-Redirect
"""

from django.http import HttpResponse
from django.shortcuts import render


class HtmxFormMixin:
    """
    Mixin untuk menangani form submission menggunakan HTMX.
    US: US-029 — HTMX form validation pattern — 422 fragment + HX-Redirect

    TUJUAN:
      - Mengembalikan HTTP 422 dengan render fragment/partial HTML jika form invalid.
      - Mengembalikan respons kosong dengan header HX-Redirect jika form valid.
      - Fallback ke perilaku default Django FormView untuk request non-HTMX.
    """

    # Nama template partial untuk HTMX (biasanya fragment form saja)
    htmx_template_name = None

    def form_valid(self, form):
        """
        Jika request dikirim via HTMX, return response kosong dengan header HX-Redirect.
        Jika non-HTMX, kembalikan perilaku default (redirect standard).
        """
        if self.request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            response["HX-Redirect"] = self.get_success_url()
            return response
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Jika request dikirim via HTMX, return HTTP 422 beserta fragment form.
        Jika non-HTMX, kembalikan perilaku default (re-render page dengan errors).
        """
        if self.request.headers.get("HX-Request") == "true":
            ctx = self.get_context_data(form=form)
            # Gunakan htmx_template_name jika didefinisikan, jika tidak fallback ke template_name
            template = self.htmx_template_name or self.template_name
            return render(self.request, template, ctx, status=422)
        return super().form_invalid(form)
