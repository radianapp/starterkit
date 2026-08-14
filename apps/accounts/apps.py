"""
App configuration untuk accounts module.
US: US-003 — Custom User model siap pakai

TUJUAN: Setup accounts app yang berisi user model, authentication, profile management.
"""

import os

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    TUJUAN: Configuration class untuk apps.accounts app.

    ALUR:
      1. Set default auto field ke BigAutoField
      2. Setup app name dan label
      3. Ready: setup signals untuk user creation
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts & Authentication"
    path = os.path.dirname(os.path.abspath(__file__))

    def ready(self):
        """
        TUJUAN: Setup signals saat Django start.

        ALUR:
          1. Import signals module → receiver decorator mendaftarkan diri otomatis
        """
        import apps.accounts.signals  # noqa: F401
