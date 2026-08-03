"""
Model untuk kredensial WebAuthn (Passkeys / Biometrik).
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class PasskeyCredential(models.Model):
    """
    Menyimpan public key dan metadata perangkat (sidik jari/kamera) untuk login WebAuthn.
    Satu user bisa memiliki beberapa kredensial (misal: HP, Laptop).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passkeys",
        verbose_name=_("user"),
    )
    name = models.CharField(
        _("device name"),
        max_length=255,
        default="Passkey Device",
        help_text=_("Nama perangkat untuk identifikasi user"),
    )
    # webauthn credential ID biasanya berupa bytes yang disimpan sebagai base64url atau hex string.
    # Kita simpan sebagai string (panjang max 255 sudah cukup untuk base64url).
    credential_id = models.CharField(
        _("credential ID"),
        max_length=255,
        unique=True,
    )
    # Public key dari perangkat (bisa cukup besar, lebih baik TextField)
    public_key = models.TextField(
        _("public key"),
    )
    sign_count = models.PositiveIntegerField(
        _("sign count"),
        default=0,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    last_used_at = models.DateTimeField(
        _("last used at"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("passkey credential")
        verbose_name_plural = _("passkey credentials")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.name}"
