"""
URL configuration untuk dashboard app.
US: US-001 — Clone & jalankan project baru

TUJUAN: Route dashboard URLs.
"""

from django.urls import path

from apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_index, name="index"),
]
