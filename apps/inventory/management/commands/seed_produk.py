from django.core.management.base import BaseCommand
from apps.inventory.models import Produk
from faker import Faker

class Command(BaseCommand):
    help = 'Seed data untuk Produk'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Jumlah data yang ingin dibuat')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker('id_ID')

        import random
        from apps.inventory.models import Kategori, Pemasok

        # Ensure we have at least one Kategori and Pemasok
        kategori, _ = Kategori.objects.get_or_create(nama="Umum")
        pemasok, _ = Pemasok.objects.get_or_create(nama="Pemasok Default")

        statuses = ["aktif", "stok_menipis", "habis", "draf"]
        
        self.stdout.write(f"Membuat {count} Produk...")

        for _ in range(count):
            Produk.objects.create(
                nama=fake.word().capitalize() + " " + fake.word().capitalize(),
                harga=random.randint(10, 1000) * 1000,
                stok=random.randint(0, 500),
                deskripsi=fake.text(),
                status=random.choice(statuses),
                kategori=kategori,
                pemasok=pemasok,
            )

        self.stdout.write(self.style.SUCCESS(f"Berhasil membuat {count} Produk."))
