"""
URL configuration untuk dashboard app.
US: US-001 — Clone & jalankan project baru

TUJUAN: Route dashboard URLs.
"""

from django.urls import path
from django.views.generic import TemplateView

app_name = "dashboard"

urlpatterns = [
    path("", TemplateView.as_view(template_name="dashboard/index.html"), name="index"),
]
