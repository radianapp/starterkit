"""
App configuration untuk dashboard module.
US: US-001 — Clone & jalankan project baru

TUJUAN: Setup dashboard app sebagai halaman utama setelah login.
"""

import os

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """
    TUJUAN: Configuration class untuk apps.dashboard app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    label = "dashboard"
    verbose_name = "Dashboard"
    path = os.path.dirname(os.path.abspath(__file__))
