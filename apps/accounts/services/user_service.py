"""
Service layer untuk user management.
US: US-004 — Register akun baru
US: US-003 — Custom User model siap pakai

TUJUAN: Logic bisnis pembuatan user — dipisahkan dari view agar bisa dipanggil
dari view, Celery task, atau management command tanpa duplikasi.

ALUR:
  1. Terima data dari wizard (email, password, extra)
  2. Buat User via create_user()
  3. Update UserProfile.extra_data dengan jawaban wizard
  4. Return user yang sudah dibuat
"""

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_from_wizard(email: str, password: str, extra: dict) -> "User":
    """
    TUJUAN: Buat User + UserProfile dari data registration wizard.

    ALUR:
      1. create_user() → signal post_save → UserProfile auto-created
      2. Update profile.extra_data dengan jawaban custom steps
      3. Return user

    DIPANGGIL DARI: apps.accounts.views.register.register_wizard (step password)
    DEPENDENSI: apps.accounts.models.User, apps.accounts.signals (auto-create profile)

    # 🧪 TEST MANUAL: Cek di Django shell:
    #   from apps.accounts.services.user_service import create_user_from_wizard
    #   u = create_user_from_wizard("test@x.com", "pass1234", {"org": "RDP"})
    #   assert u.profile.extra_data == {"org": "RDP"}
    """
    # Import di dalam fungsi untuk hindari circular import pada test
    from apps.accounts.models import UserProfile

    # Gunakan email sebagai username — unique constraint di User.email sudah cukup
    user = User.objects.create_user(
        email=email,
        password=password,
        username=email,
    )

    if extra:
        # Signal sudah buat profile kosong — update extra_data saja
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.extra_data = extra
        profile.save(update_fields=["extra_data"])

    return user
