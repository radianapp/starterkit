"""
Signals untuk accounts app.
US: US-003 — Custom User model siap pakai
US: US-004 — Register akun baru

TUJUAN: Auto-create UserProfile saat User baru dibuat.

ALUR:
  1. Signal post_save pada User model
  2. Jika created=True → buat UserProfile otomatis
  3. Dipanggil dari AccountsConfig.ready()
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    TUJUAN: Buat UserProfile otomatis saat User baru dibuat.

    ALUR:
      1. Cek apakah ini create baru (bukan update)
      2. Buat UserProfile dengan user=instance
      3. Profile dibuat kosong — diisi via wizard atau edit profil

    DIPANGGIL DARI: AccountsConfig.ready() via signal post_save
    DEPENDENSI: apps.accounts.models.UserProfile
    """
    # Import di sini untuk hindari circular import
    from apps.accounts.models import UserProfile

    if created:
        UserProfile.objects.get_or_create(user=instance)
