import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Menampilkan versi aktif aplikasi saat ini (App Version)"

    def handle(self, *args, **kwargs):
        version = getattr(settings, "LOCAL_APP_VERSION", "1.0.0")
        updated_at = getattr(settings, "LOCAL_APP_VERSION_DATE", "Unknown")
        updated_by = getattr(settings, "LOCAL_APP_VERSION_BY", "Unknown")
        description = getattr(settings, "LOCAL_APP_VERSION_DESC", "")

        self.stdout.write(self.style.SUCCESS(f"Aplikasi Versi : v{version}"))
        self.stdout.write(f"Diperbarui Pada: {updated_at}")
        self.stdout.write(f"Diperbarui Oleh: {updated_by}")
        if description:
            self.stdout.write(f"Keterangan     : {description}")
        self.stdout.write(self.style.MIGRATE_HEADING("---"))
        self.stdout.write(self.style.WARNING("Gunakan perintah .\\bin\\app-version.ps1 atau ./bin/app-version.sh untuk menaikkan versi."))
