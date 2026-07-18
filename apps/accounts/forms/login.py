"""
Form untuk login.
US: US-005 — Login

TUJUAN: Validasi identifier (email atau username) + password saat login.

ALUR:
  1. Input identifier (email atau username) dan password
  2. Autentikasi user — dicoba via email dulu, fallback ke username
  3. Cek user aktif (is_active)

DIPANGGIL DARI: apps.accounts.views.login.user_login
"""

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    """
    TUJUAN: Form login yang menerima email atau username sebagai identifier.

    ALUR:
      1. Terima identifier (email/username) + password
      2. clean() → authenticate() via EmailOrUsernameBackend → set self.user jika valid
      3. View ambil self.user untuk login()

    DIPANGGIL DARI: apps.accounts.views.login.user_login
    """

    identifier = forms.CharField(
        label=_("Email atau Username"),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "placeholder": _("nama@contoh.com atau username"),
            }
        ),
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
          1. Ambil identifier + password dari cleaned_data
          2. authenticate() — memanggil EmailOrUsernameBackend
             (coba email dulu, fallback ke username)
          3. Cek user.is_active
          4. Simpan ke self.user untuk diambil view

        CATATAN: authenticate() meneruskan 'identifier' sebagai 'username'
                 ke backend karena itulah konvensi Django.
        """
        cleaned = super().clean()
        identifier = cleaned.get("identifier", "").strip()
        password = cleaned.get("password", "")

        if identifier and password:
            self.user = authenticate(self.request, username=identifier, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    _("Email/username atau password salah. Silakan coba lagi."),
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

        DIPANGGIL DARI: apps.accounts.views.login.user_login
        """
        return self.user
