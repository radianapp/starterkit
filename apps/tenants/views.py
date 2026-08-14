"""
Views handler untuk aksi multi-tenancy & tenant switcher.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View

from apps.tenants.services import switch_active_tenant


class SwitchTenantView(LoginRequiredMixin, View):
    """
    POST endpoint untuk berpindah tenant aktif.
    """

    def post(self, request, *args, **kwargs):
        tenant_id = request.POST.get("tenant_id")
        if tenant_id:
            switch_active_tenant(request, tenant_id)

        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"

        # Support HTMX redirect header
        if request.headers.get("HX-Request"):
            response = redirect(next_url)
            response["HX-Redirect"] = next_url
            return response

        return HttpResponseRedirect(next_url)
