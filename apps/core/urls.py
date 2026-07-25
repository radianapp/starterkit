"""
URL patterns untuk apps.core (Documentation, Examples, HTMX Demo, Public Pages).
"""

from django.urls import path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # Halaman Publik (US-031)
    path("about/", TemplateView.as_view(template_name="public/about.html"), name="about"),
    path("terms/", TemplateView.as_view(template_name="public/terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="public/privacy.html"), name="privacy"),

    # Redirects RDP-UI
    path("rdp-ui/", RedirectView.as_view(url="https://ui.radian.web.id", permanent=False), name="rdp-ui-landing"),
    path("rdp-ui/tokens/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_token_test"),
    path("rdp-ui/layout/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_layout_test"),
    path("rdp-ui/components/", RedirectView.as_view(url="https://ui.radian.web.id/docs/", permanent=False), name="rdp_ui_components_test"),
]

# Modul starter views (hanya aktif jika demo pages ada & starter.py terpasang)
try:
    from apps.core.views.starter import (
        StarterComponentsView,
        StarterDocsView,
        StarterExamplesView,
        StarterLayoutView,
    )

    urlpatterns += [
        path("docs/", StarterDocsView.as_view(), name="docs_index"),
        path("examples/", StarterExamplesView.as_view(), name="examples_index"),
        path("examples/layout/", StarterLayoutView.as_view(), name="examples_layout"),
        path("examples/components/", StarterComponentsView.as_view(), name="examples_components"),
        path("starter/layout/", RedirectView.as_view(url="/examples/layout/", permanent=True), name="starter_layout"),
        path("starter/components/", RedirectView.as_view(url="/examples/components/", permanent=True), name="starter_components"),
        path("starter/cli/", RedirectView.as_view(url="/docs/#cli", permanent=True), name="starter_cli"),
        path("starter/auth/", RedirectView.as_view(url="/accounts/login/", permanent=True), name="starter_auth"),
        path("starter/dashboard/", RedirectView.as_view(url="/dashboard/", permanent=True), name="starter_dashboard"),
    ]
except ImportError:
    pass

# Modul HTMX examples (hanya aktif jika demo pages ada & htmx_examples.py terpasang)
try:
    from apps.core.views.htmx_examples import (
        ContactCreateView,
        ContactDeleteView,
        ContactInlineEditView,
        ContactSearchView,
        HtmxExamplesIndexView,
        InfiniteScrollRowsView,
        InfiniteScrollView,
        JobStatusPollingView,
        LiveValidationView,
        ToastDemoView,
    )

    urlpatterns += [
        path("examples/htmx/", HtmxExamplesIndexView.as_view(), name="htmx-examples"),
        path("examples/htmx/contact/create/", ContactCreateView.as_view(), name="htmx-contact-create"),
        path("examples/htmx/contact/delete/<int:pk>/", ContactDeleteView.as_view(), name="htmx-contact-delete"),
        path("examples/htmx/contact/edit/<int:pk>/", ContactInlineEditView.as_view(), name="htmx-contact-edit"),
        path("examples/htmx/toast/demo/", ToastDemoView.as_view(), name="htmx-toast-demo"),
        path("examples/htmx/contact/search/", ContactSearchView.as_view(), name="htmx-contact-search"),
        path("examples/htmx/validate/email/", LiveValidationView.as_view(), name="htmx-live-validation"),
        path("examples/htmx/infinite-scroll/", InfiniteScrollView.as_view(), name="htmx-infinite-scroll"),
        path("examples/htmx/infinite-scroll/rows/", InfiniteScrollRowsView.as_view(), name="htmx-infinite-scroll-rows"),
        path("examples/htmx/polling/", JobStatusPollingView.as_view(), name="htmx-polling"),
    ]
except ImportError:
    pass
