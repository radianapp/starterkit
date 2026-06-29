"""
App configuration untuk core module.
US: US-001 — Clone & jalankan project baru

TUJUAN: Setup core app yang berisi utils, mixins, base views, context processors.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    TUJUAN: Configuration class untuk apps.core app.

    ALUR:
      1. Set default auto field ke BigAutoField
      2. Setup app name dan label
      3. Ready: setup signals dan initialization saat Django start
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = "Core"

    def ready(self):
        """
        TUJUAN: Setup signals dan initialization saat Django start.

        ALUR:
          1. Import signals (jika ada)
          2. Register signal handlers
        """
        pass
