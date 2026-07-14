"""
Model Activity untuk dashboard app.
US: US-032 — Dashboard default dengan demo data
"""

import typing

from django.conf import settings
from django.db import models


class Activity(models.Model):
    """
    Model Activity untuk mencatat aktivitas / transaksi dummy di dashboard.
    US: US-032 — Dashboard default dengan demo data
    """

    STATUS_CHOICES: typing.ClassVar[list[tuple[str, str]]] = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name="Pengguna",
    )
    title = models.CharField(max_length=255, verbose_name="Judul Aktivitas")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Status",
    )
    amount = models.DecimalField(
        max_length=20,
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Jumlah/Nilai",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    class Meta:
        verbose_name = "Aktivitas"
        verbose_name_plural = "Daftar Aktivitas"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.status} ({self.amount})"
