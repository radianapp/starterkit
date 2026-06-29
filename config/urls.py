"""
Root URL configuration untuk RDP Starter Kit.
US: US-015 — Error pages kustom (403, 404, 500)

TUJUAN: Route semua request ke app-specific URLs, setup error page handlers.
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

# Serve media files di development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # ⚙️ KONFIGURASI: Debug toolbar untuk development
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns

# ⚙️ KONFIGURASI: Error handlers
# KEPUTUSAN TEKNIS: Setup custom error handlers untuk 403, 404, 500
# ALASAN: Memberikan UX yang konsisten dengan branding project
# ALTERNATIF: Gunakan default Django error pages (kurang custom)
handler403 = "apps.core.views.error.permission_denied_view"
handler404 = "apps.core.views.error.page_not_found_view"
handler500 = "apps.core.views.error.server_error_view"
