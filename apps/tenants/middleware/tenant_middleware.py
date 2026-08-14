"""
TenantMiddleware: Middleware penentu tenant/organisasi aktif pada HTTP request.
US: US-027 — Multi-Tenancy Subdomain & Session Context Isolation
"""

from django.conf import settings

from apps.tenants.models import Organization


class TenantMiddleware:
    """
    Middleware yang memeriksa apakah Multi-Tenancy diaktifkan (via RDP_MULTI_TENANCY_ENABLED).
    Jika aktif, mendeteksi tenant dari subdomain atau session context, lalu menempelkan request.tenant.
    Jika nonaktif, menetapkan request.tenant = None.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Cek toggle .env / settings
        is_multi_tenancy_enabled = getattr(settings, "RDP_MULTI_TENANCY_ENABLED", False)

        if not is_multi_tenancy_enabled:
            request.tenant = None
            request.is_multi_tenancy_enabled = False
            return self.get_response(request)

        request.is_multi_tenancy_enabled = True
        request.tenant = self._resolve_tenant(request)

        response = self.get_response(request)
        return response

    def _resolve_tenant(self, request):
        """Mendeteksi instance Organization berdasarkan subdomain, session, atau user fallback."""
        host = request.get_host().split(":")[0]  # strip port
        host_parts = host.split(".")

        # Subdomain detection (e.g. acme.localhost or acme.domain.com)
        if len(host_parts) >= 2 and host_parts[0] not in ("www", "localhost", "127"):
            subdomain_slug = host_parts[0].lower()
            org = Organization.objects.filter(slug=subdomain_slug, is_active=True).first()
            if org:
                return org

        # Session context detection
        active_tenant_id = request.session.get("active_tenant_id")
        if active_tenant_id:
            org = Organization.objects.filter(id=active_tenant_id, is_active=True).first()
            if org:
                return org

        # Fallback to user's first organization
        if hasattr(request, "user") and request.user.is_authenticated:
            membership = (
                request.user.organization_memberships.select_related("organization")
                .filter(organization__is_active=True)
                .first()
            )
            if membership:
                org = membership.organization
                request.session["active_tenant_id"] = org.id
                return org

        return None
