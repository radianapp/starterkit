import os

from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.test_app"
    path = os.path.dirname(os.path.abspath(__file__))
