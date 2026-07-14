"""
Form untuk login.
US: US-005 — Login

TUJUAN: Validasi email + password saat login.

ALUR:
  1. Input email dan password
  2. Validasi format email
  3. Autentikasi user (cek credentials di DB)
  4. Cek user aktif (is_active)

DIPANGGIL DARI: apps.accounts.views.login.UserLoginView
"""

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    """
    TUJUAN: Form login dengan email dan password.

    ALUR:
      1. Terima email + password
      2. clean() → authenticate() → set self.user jika valid
      3. View ambil self.user untuk login()

    DIPANGGIL DARI: apps.accounts.views.login.UserLoginView
    """

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    remember_me = forms.BooleanField(
        label=_("Ingat saya"),
        required=False,
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        TUJUAN: Simpan request untuk kebutuhan authenticate().
        """
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        TUJUAN: Autentikasi credentials dan set self.user.

        ALUR:
          1. Ambil email + password dari cleaned_data
          2. authenticate() — return user atau None
          3. Cek user.is_active
          4. Simpan ke self.user untuk diambil view
        """
        cleaned = super().clean()
        email = cleaned.get("email", "").lower().strip()
        password = cleaned.get("password", "")

        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    _("Email atau password salah. Silakan coba lagi."),
                    code="invalid_login",
                )
            if not self.user.is_active:
                raise forms.ValidationError(
                    _("Akun ini tidak aktif."),
                    code="inactive",
                )
        return cleaned

    def get_user(self):
        """
        TUJUAN: Return authenticated user setelah form valid.

        DIPANGGIL DARI: apps.accounts.views.login.UserLoginView.form_valid()
        """
        return self.user
