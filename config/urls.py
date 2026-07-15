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

from apps.core.views import RdpUiComponentsTestView, RdpUiLayoutTestView, RdpUiTokenTestView
from apps.core.views import htmx_examples as htmx_views


def home_view(request):
    """Redirect ke dashboard jika sudah login, tampilkan landing page jika belum."""
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    return TemplateView.as_view(template_name="home.html")(request)


urlpatterns = [
    # Root → landing page publik (redirect dashboard jika sudah login)
    path("", home_view, name="home"),

    # RDP-UI Landing sudah digabung ke /. Redirect agar tidak ada broken link.
    path("rdp-ui/", RedirectView.as_view(url="/", permanent=False), name="rdp-ui-landing"),

    # RDP-UI Token & Theme Showcase (Phase 1 & 2)
    path("rdp-ui/tokens/", RdpUiTokenTestView.as_view(), name="rdp_ui_token_test"),
    path("rdp-ui/layout/", RdpUiLayoutTestView.as_view(), name="rdp_ui_layout_test"),
    path("rdp-ui/components/", RdpUiComponentsTestView.as_view(), name="rdp_ui_components_test"),

    # Halaman Publik (US-031)
    path("about/", TemplateView.as_view(template_name="public/about.html"), name="about"),
    path("terms/", TemplateView.as_view(template_name="public/terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="public/privacy.html"), name="privacy"),

    # Showcase 10 Pola HTMX (US-036)
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
