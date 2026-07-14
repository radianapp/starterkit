"""
Management command to load demo data.
US: US-037 — Management command demo data
"""

import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.dashboard.models.activity import Activity

User = get_user_model()


class Command(BaseCommand):
    """
    TUJUAN: Membuat sample user (superuser + regular) dan data aktivitas dummy secara idempotent.
    US: US-037 — Management command demo data
    """

    help = "Membuat data contoh/demo secara idempotent untuk pengujian dashboard dan UI."

    def handle(self, *args, **options):
        self.stdout.write("Menyiapkan data demo...")

        # 1. Buat Superuser (Admin)
        admin_email = "admin@rdp.test"
        admin_user, created_admin = User.objects.get_or_create(
            username=admin_email,
            email=admin_email,
            defaults={
                "first_name": "Admin",
                "last_name": "RDP",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created_admin:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Superuser baru dibuat: {admin_email} (password: admin123)")
            )
        else:
            self.stdout.write(f"Superuser '{admin_email}' sudah ada.")

        # 2. Buat Regular Users
        regular_users = [
            ("user1@rdp.test", "Rahadi", "Putra"),
            ("user2@rdp.test", "Budi", "Santoso"),
        ]
        users_instances = []

        # Tambahkan admin ke pool agar aktivitas tersebar
        users_instances.append(admin_user)

        for email, first, last in regular_users:
            user, created = User.objects.get_or_create(
                username=email,
                email=email,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "is_staff": False,
                    "is_superuser": False,
                },
            )
            if created:
                user.set_password("user123")
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"User baru dibuat: {email} (password: user123)")
                )
            else:
                self.stdout.write(f"User '{email}' sudah ada.")
            users_instances.append(user)

        # 3. Buat Data Aktivitas Dummy (Min 15 item agar teruji pagination > 10 baris)
        sample_activities = [
            ("Registrasi Pengguna Baru", "Pendaftaran akun baru di platform", "completed", 0.00),
            (
                "Pembayaran Invoice INV-2026-001",
                "Pembayaran layanan cloud hosting bulanan",
                "completed",
                150000.00,
            ),
            ("Integrasi API Payment Gateway", "Setup koneksi merchant Midtrans", "pending", 0.00),
            ("Pembelian Lisensi Tambahan", "Upgrade ke paket Enterprise", "completed", 500000.00),
            (
                "Sinkronisasi Database Otomatis",
                "Pencadangan harian ke cloud storage GCS",
                "completed",
                0.00,
            ),
            ("Klaim Refund Layanan", "Gagal deploy di zona asia-southeast2", "failed", 75000.00),
            ("Konfigurasi SSL Domain", "Pembaruan sertifikat let's encrypt", "completed", 0.00),
            (
                "Pembayaran Invoice INV-2026-002",
                "Pembelian add-on analytics dashboard",
                "completed",
                250000.00,
            ),
            ("Audit Keamanan Bulanan", "Pemeriksaan celah OWASP Top 10", "pending", 0.00),
            ("Upgrade Paket Storage", "Kapasitas tambahan 100GB", "completed", 120000.00),
            (
                "Pengiriman Laporan Keuangan",
                "Laporan dikirim ke finance@radian.web.id",
                "completed",
                0.00,
            ),
            (
                "Penyelidikan Bug Latensi",
                "Response time lambat pada API endpoint auth",
                "failed",
                0.00,
            ),
            ("Setup Environment Staging", "Inisialisasi server testing baru", "completed", 0.00),
            (
                "Pembaruan Profil Perusahaan",
                "Mengubah logo dan deskripsi kontak utama",
                "completed",
                0.00,
            ),
            ("Pendaftaran Uji Coba Beta", "Beta testing untuk fitur CLI rdp new", "pending", 0.00),
            ("Perpanjangan Layanan Hosting", "Invoice INV-2026-003", "completed", 150000.00),
        ]

        activities_created = 0
        for title, desc, status, amount in sample_activities:
            # Agar timestamp sedikit berbeda untuk urutan pagination
            # Gunakan get_or_create berdasarkan kombinasi title dan deskripsi
            _, created = Activity.objects.get_or_create(
                title=title,
                description=desc,
                defaults={
                    "user": random.choice(users_instances),
                    "status": status,
                    "amount": Decimal(str(amount)),
                },
            )
            if created:
                activities_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Selesai! Berhasil memuat data demo: {activities_created} aktivitas baru dibuat."
            )
        )
