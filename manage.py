#!/usr/bin/env python
"""
Django management script untuk RDP Starter Kit.
US: US-001 — Clone & jalankan project baru
"""

import os
import sys


def main():
    """
    TUJUAN: Run administrative tasks untuk Django project.

    ALUR:
      1. Set DJANGO_SETTINGS_MODULE dari environment (default: config.settings.dev)
      2. Parse command line arguments
      3. Execute Django management command
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
