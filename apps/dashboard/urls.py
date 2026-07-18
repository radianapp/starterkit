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
    path("api/stats/", views.dashboard_stats_htmx, name="stats"),
    path("changelog/", views.SystemUpdateListView.as_view(), name="changelog"),
]
