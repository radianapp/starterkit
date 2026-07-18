"""
Custom authentication backend untuk mendukung login dengan email atau username.
US: US-005 — Login

TUJUAN:
  Mengizinkan user untuk login menggunakan email ATAU username.
  Django secara default hanya mendukung satu field sebagai username (USERNAME_FIELD).
  Backend ini menambahkan kemampuan lookup via username jika login via email gagal.

ALUR:
  1. Coba temukan user berdasarkan email (karena USERNAME_FIELD = 'email')
  2. Jika tidak ditemukan via email, coba cari via username
  3. Validasi password
  4. Return user jika valid, None jika tidak

DIPANGGIL DARI: apps.accounts.forms.login.LoginForm.clean()
  via django.contrib.auth.authenticate() dengan backend ini terdaftar di AUTHENTICATION_BACKENDS
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Authentication backend yang mendukung login dengan email atau username.

    ALUR:
      1. Coba lookup user berdasarkan field 'identifier' (bisa email atau username)
      2. Jika ditemukan, validasi password
      3. Return user jika valid dan aktif

    DIPANGGIL DARI: django.contrib.auth.authenticate()
    """

    def authenticate(self, request, username: str | None = None, password: str | None = None, **kwargs):
        """
        TUJUAN: Autentikasi user berdasarkan email atau username.

        ALUR:
          1. Tidak ada identifier → return None
          2. Coba cari user via email (case-insensitive)
          3. Jika tidak ada, coba cari via username (case-insensitive)
          4. Jika user ditemukan, validasi password dengan check_password()
          5. Return user atau None

        CATATAN: Parameter 'username' digunakan karena Django memanggil backend
                 dengan parameter ini secara default dari authenticate().
        """
        if username is None:
            return None

        identifier = username.strip()
        user = None

        # 1. Coba cari via email (case-insensitive)
        try:
            user = User.objects.get(email__iexact=identifier)
        except User.DoesNotExist:
            pass

        # 2. Jika tidak ditemukan via email, coba via username
        if user is None:
            try:
                user = User.objects.get(username__iexact=identifier)
            except User.DoesNotExist:
                # Jalankan default hasher untuk mencegah timing attack
                User().set_password(password)
                return None

        # 3. Validasi password dan status user
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
