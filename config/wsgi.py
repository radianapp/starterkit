"""
WSGI config untuk RDP Starter Kit.
US: US-001 — Clone & jalankan project baru

TUJUAN: Entry point untuk WSGI server (Gunicorn).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

application = get_wsgi_application()
