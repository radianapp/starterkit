"""
Root URL configuration untuk RDP Starter Kit.
US: US-015 — Error pages kustom (403, 404, 500)

TUJUAN: Route semua request ke app-specific URLs secara dinamis berdasarkan INSTALLED_APPS, setup error page handlers.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def is_app_installed(app_module_name: str) -> bool:
    """Periksa apakah app terdaftar di settings.INSTALLED_APPS (baik string module maupun AppConfig class path)."""
    return any(
        app == app_module_name or app.startswith(f"{app_module_name}.")
        for app in settings.INSTALLED_APPS
    )


def home_view(request):
    """
    Root URL redirect:
    - Jika user sudah login dan apps.dashboard terpasang -> redirect ke dashboard
    - Jika template home.html ada -> tampilkan landing page publik
    - Jika home.html tidak ada (landing page dinonaktifkan) -> redirect ke login page
    """
    if request.user.is_authenticated and is_app_installed("apps.dashboard"):
        return redirect("dashboard:index")

    from django.template.loader import TemplateDoesNotExist, get_template

    try:
        get_template("home.html")
        return TemplateView.as_view(template_name="home.html")(request)
    except TemplateDoesNotExist:
        if is_app_installed("apps.accounts"):
            return redirect("accounts:login")
        elif is_app_installed("apps.dashboard"):
            return redirect("dashboard:index")
        return redirect("admin:index")



urlpatterns = [
    # Root → landing page publik (redirect dashboard jika sudah login)
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
]

# Dinamis mendaftarkan URL aplikasi berdasarkan INSTALLED_APPS
if is_app_installed("apps.core"):
    urlpatterns.append(path("", include("apps.core.urls")))

if is_app_installed("apps.accounts"):
    urlpatterns.append(path("accounts/", include("apps.accounts.urls")))

if is_app_installed("apps.dashboard"):
    urlpatterns.append(path("dashboard/", include("apps.dashboard.urls")))

if is_app_installed("apps.inventory"):
    urlpatterns.append(path("produk/", include("apps.inventory.urls")))

# Global API Router & Documentation
urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("config.api_urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve media files di development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # ⚙️ KONFIGURASI: Debug toolbar untuk development
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls")), *urlpatterns]

    # Halaman internal demo komponen dev
    try:
        from apps.core.views import DevComponentsView

        urlpatterns += [
            path("dev/components/", DevComponentsView.as_view(), name="dev-components"),
        ]
    except ImportError:
        pass

# ⚙️ KONFIGURASI: Error handlers
handler403 = "apps.core.views.error.permission_denied_view"
handler404 = "apps.core.views.error.page_not_found_view"
handler500 = "apps.core.views.error.server_error_view"
