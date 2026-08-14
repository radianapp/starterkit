"""
Service layer untuk pengaturan (settings) aplikasi.

TUJUAN: Menyimpan dan mengambil preferensi pengguna dari UserProfile.extra_data.
"""

from apps.accounts.models.profile import UserProfile


def update_user_preferences(user, data: dict) -> UserProfile:
    """
    TUJUAN: Perbarui pengaturan/preferensi user (tema, row per page, dll) ke dalam extra_data.

    ALUR:
      1. Ambil atau buat UserProfile untuk user ini.
      2. Gabungkan data baru dengan extra_data yang sudah ada.
      3. Simpan perubahan ke database.
    """
    profile, _ = UserProfile.objects.get_or_create(user=user)

    current_data = profile.extra_data or {}
    for key, value in data.items():
        current_data[key] = value

    profile.extra_data = current_data
    profile.save(update_fields=["extra_data"])
    return profile


def get_user_preference(user, key: str, default=None):
    """
    TUJUAN: Ambil nilai preferensi pengguna berdasarkan kunci (key).
    """
    if not hasattr(user, "profile"):
        return default
    return user.profile.extra_data.get(key, default)
