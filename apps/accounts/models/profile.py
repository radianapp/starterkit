"""
UserProfile model untuk extended user information.
US: US-009 — Edit profil & avatar

TUJUAN: OneToOne relation ke User untuk menyimpan profile data (avatar, bio, preferences).

ALUR:
  1. Create OneToOne field ke User model
  2. Tambah avatar field dengan image storage
  3. Tambah timestamps
  4. Auto-create profile saat user baru
"""

from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class UserProfile(models.Model):
    """
    TUJUAN: Extended profile information untuk setiap User.

    ALUR:
      1. OneToOne ke User — satu profile per user
      2. Avatar (image) — store foto profil
      3. Bio dan preferences — extra fields untuk future expansion

    DIPANGGIL DARI: apps.accounts.models.__init__.py, signals untuk auto-create
    DEPENDENSI: apps.accounts.models.user.User
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
        verbose_name=_("user"),
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/%Y/%m/%d/",
        null=True,
        blank=True,
        help_text=_("Foto profil user (max 2MB, JPG/PNG)"),
    )
    bio = models.TextField(
        _("bio"),
        blank=True,
        max_length=500,
        help_text=_("Deskripsi singkat tentang user"),
    )
    # KEPUTUSAN TEKNIS: Simpan jawaban wizard registration di JSONField
    # ALASAN: Tiap project punya step custom berbeda — skema tidak bisa diprediksi di model
    # ALTERNATIF: Buat model terpisah per step, tapi overengineering untuk starter kit
    extra_data = models.JSONField(
        _("extra data"),
        default=dict,
        blank=True,
        help_text=_("Data tambahan dari registration wizard (konfigurasi via REGISTRATION_STEPS)"),
    )

    # Timestamps
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering: ClassVar[list] = ["-created_at"]

    def __str__(self):
        """Return username sebagai string representation."""
        return f"Profile: {self.user.email}"

    def get_avatar_url(self):
        """
        TUJUAN: Return avatar URL atau default placeholder.

        ALUR:
          1. Jika avatar ada, return avatar.url
          2. Jika tidak, return default placeholder URL atau generate inisial

        DIPANGGIL DARI: templates/base.html navbar, profil view
        DEPENDENSI: self.avatar
        """
        if self.avatar:
            return self.avatar.url
        # TODO: Return default avatar atau inisial user
        return "/static/images/default-avatar.png"
