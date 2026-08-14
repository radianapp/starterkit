from django.urls import path

from apps.tenants.views import SwitchTenantView

app_name = "tenants"

urlpatterns = [
    path("switch/", SwitchTenantView.as_view(), name="switch"),
]
