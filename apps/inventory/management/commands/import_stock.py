from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deskripsi command import_stock'

    def add_arguments(self, parser):
        # parser.add_argument('--force', action='store_true', help='Force execution')
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Command import_stock berhasil dijalankan.'))
