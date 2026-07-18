"""
Root URL configuration untuk RDP Starter Kit.
US: US-015 — Error pages kustom (403, 404, 500)

TUJUAN: Route semua request ke app-specific URLs, setup error page handlers.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.core.views import StarterDocsView, StarterExamplesView, StarterComponentsView, StarterLayoutView
from apps.core.views import htmx_examples as htmx_views


def home_view(request):
    """Redirect ke dashboard jika sudah login, tampilkan landing page jika belum."""
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    return TemplateView.as_view(template_name="home.html")(request)


urlpatterns = [
    # Root → landing page publik (redirect dashboard jika sudah login)
    path("", home_view, name="home"),

    # Docs & Examples — 2 halaman utama navbar
    path("docs/", StarterDocsView.as_view(), name="docs_index"),
    path("examples/", StarterExamplesView.as_view(), name="examples_index"),

    # Examples sub-pages
    path("examples/layout/", StarterLayoutView.as_view(), name="examples_layout"),
    path("examples/components/", StarterComponentsView.as_view(), name="examples_components"),

    # Redirect lama agar tidak 404
    path("starter/layout/", RedirectView.as_view(url="/examples/layout/", permanent=True), name="starter_layout"),
    path("starter/components/", RedirectView.as_view(url="/examples/components/", permanent=True), name="starter_components"),
    path("starter/cli/", RedirectView.as_view(url="/docs/#cli", permanent=True), name="starter_cli"),
    path("starter/auth/", RedirectView.as_view(url="/accounts/login/", permanent=True), name="starter_auth"),
    path("starter/dashboard/", RedirectView.as_view(url="/dashboard/", permanent=True), name="starter_dashboard"),
    path("rdp-ui/", RedirectView.as_view(url="https://ui.radian.web.id", permanent=False), name="rdp-ui-landing"),
    path("rdp-ui/tokens/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_token_test"),
    path("rdp-ui/layout/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_layout_test"),
    path("rdp-ui/components/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_components_test"),

    # Halaman Publik (US-031)
    path("about/", TemplateView.as_view(template_name="public/about.html"), name="about"),
    path("terms/", TemplateView.as_view(template_name="public/terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="public/privacy.html"), name="privacy"),

    # HTMX Examples (US-036)
    path("examples/htmx/", htmx_views.HtmxExamplesIndexView.as_view(), name="htmx-examples"),
    path(
        "examples/htmx/contact/create/",
        htmx_views.ContactCreateView.as_view(),
        name="htmx-contact-create",
    ),
    path(
        "examples/htmx/contact/delete/<int:pk>/",
        htmx_views.ContactDeleteView.as_view(),
        name="htmx-contact-delete",
    ),
    path(
        "examples/htmx/contact/edit/<int:pk>/",
        htmx_views.ContactInlineEditView.as_view(),
        name="htmx-contact-edit",
    ),
    path(
        "examples/htmx/toast/demo/",
        htmx_views.ToastDemoView.as_view(),
        name="htmx-toast-demo",
    ),
    path(
        "examples/htmx/contact/search/",
        htmx_views.ContactSearchView.as_view(),
        name="htmx-contact-search",
    ),
    path(
        "examples/htmx/validate/email/",
        htmx_views.LiveValidationView.as_view(),
        name="htmx-live-validation",
    ),
    path(
        "examples/htmx/infinite-scroll/",
        htmx_views.InfiniteScrollView.as_view(),
        name="htmx-infinite-scroll",
    ),
    path(
        "examples/htmx/infinite-scroll/rows/",
        htmx_views.InfiniteScrollRowsView.as_view(),
        name="htmx-infinite-scroll-rows",
    ),
    path("examples/htmx/polling/", htmx_views.JobStatusPollingView.as_view(), name="htmx-polling"),

    # App URLs
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("api-auth/", include("rest_framework.urls")),

    # API v1 Global Router
    path("api/v1/", include("config.api_urls")),

    # API Documentation (drf-spectacular)
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

    # Halaman internal demo komponen
    from apps.core.views import DevComponentsView

    urlpatterns += [
        path("dev/components/", DevComponentsView.as_view(), name="dev-components"),
    ]

# ⚙️ KONFIGURASI: Error handlers
# KEPUTUSAN TEKNIS: Setup custom error handlers untuk 403, 404, 500
# ALASAN: Memberikan UX yang konsisten dengan branding project
# ALTERNATIF: Gunakan default Django error pages (kurang custom)
handler403 = "apps.core.views.error.permission_denied_view"
handler404 = "apps.core.views.error.page_not_found_view"
handler500 = "apps.core.views.error.server_error_view"
