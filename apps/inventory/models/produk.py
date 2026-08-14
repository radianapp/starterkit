# apps/inventory/models/produk.py
# US-CRUD-01: Model Produk untuk demo CRUD Dashboard

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Kategori(models.Model):
    """
    TUJUAN: Kategori produk untuk filter dan grouping.

    DIPANGGIL DARI: Produk (FK), views/produk.py
    """

    nama = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nama"]
        verbose_name_plural = "Kategori"

    def __str__(self):
        return self.nama


class Pemasok(models.Model):
    """
    TUJUAN: Data pemasok/supplier produk.

    DIPANGGIL DARI: Produk (FK), views/produk.py
    """

    nama = models.CharField(max_length=200)

    class Meta:
        ordering = ["nama"]
        verbose_name_plural = "Pemasok"

    def __str__(self):
        return self.nama


class Produk(models.Model):
    """
    TUJUAN: Model produk utama — demo CRUD dashboard.

    ALUR:
      1. User tambah produk via modal
      2. Status dihitung otomatis dari stok
      3. List tampil di tabel dengan filter/search

    DIPANGGIL DARI: views/produk.py, admin/produk_admin.py
    DEPENDENSI: Kategori, Pemasok
    """

    STATUS_CHOICES = [
        ("aktif", "Aktif"),
        ("stok_menipis", "Stok Menipis"),
        ("habis", "Habis"),
        ("draf", "Draf"),
    ]

    # KEPUTUSAN TEKNIS: SKU nullable untuk auto-generate saat save
    # ALASAN: Design spec menunjukkan "Kosongkan untuk dibuat otomatis"
    nama = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    kategori = models.ForeignKey(
        Kategori, on_delete=models.SET_NULL, null=True, blank=True, related_name="produk"
    )
    harga = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    stok = models.IntegerField(default=0)
    pemasok = models.ForeignKey(
        Pemasok, on_delete=models.SET_NULL, null=True, blank=True, related_name="produk"
    )
    deskripsi = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="aktif")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Log Aktivitas via django-simple-history
    history = HistoricalRecords()

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Produk"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        # Auto-generate SKU jika kosong
        if not self.sku:
            super().save(*args, **kwargs)
            self.sku = f"PL-{self.pk:04d}"
            Produk.objects.filter(pk=self.pk).update(sku=self.sku)
        else:
            super().save(*args, **kwargs)
