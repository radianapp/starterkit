"""
Model untuk Two-Factor Authentication (TOTP / Google Authenticator) dan Backup Codes.
US: US-043 — Two-Factor Authentication (2FA TOTP)
"""

from typing import ClassVar

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TOTPDevice(models.Model):
    """
    Menyimpan secret key Base32 untuk TOTP (Google Authenticator) per user.
    Setiap user memiliki maksimal satu active TOTPDevice.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="totp_device",
        verbose_name=_("user"),
    )
    secret_key = models.CharField(
        _("secret key"),
        max_length=64,
        help_text=_("Base32 encoded secret key untuk TOTP generation"),
    )
    is_confirmed = models.BooleanField(
        _("is confirmed"),
        default=False,
        help_text=_("Apakah perangkat sudah berhasil diverifikasi dengan token pertama"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    last_used_at = models.DateTimeField(
        _("last used at"),
        null=True,
        blank=True,
        help_text=_("Timestamp penggunaan token terakhir untuk mencegah replay attack"),
    )

    class Meta:
        verbose_name = _("TOTP device")
        verbose_name_plural = _("TOTP devices")
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        status = "Active" if self.is_confirmed else "Pending"
        return f"TOTP Device ({self.user.email}) - {status}"


class TOTPBackupCode(models.Model):
    """
    Menyimpan recovery / backup code sekali pakai jika pengguna kehilangan akses ke aplikasi authenticator.
    Nilai code disimpan dalam bentuk hash (make_password) untuk keamanan tinggi.
    """

    device = models.ForeignKey(
        TOTPDevice,
        on_delete=models.CASCADE,
        related_name="backup_codes",
        verbose_name=_("TOTP device"),
    )
    code_hash = models.CharField(
        _("code hash"),
        max_length=255,
        help_text=_("Hashed backup code untuk verifikasi sekali pakai"),
    )
    is_used = models.BooleanField(
        _("is used"),
        default=False,
        help_text=_("Status apakah kode pemulihan ini sudah digunakan"),
    )
    used_at = models.DateTimeField(
        _("used at"),
        null=True,
        blank=True,
        help_text=_("Waktu saat kode cadangan digunakan"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("TOTP backup code")
        verbose_name_plural = _("TOTP backup codes")
        ordering: ClassVar[list] = ["is_used", "-created_at"]

    def __str__(self):
        status = "Used" if self.is_used else "Available"
        return f"Backup Code for {self.device.user.email} - {status}"
