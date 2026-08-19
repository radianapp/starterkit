"""
Forms untuk Two-Factor Authentication (TOTP / Google Authenticator).
US: US-043 — Two-Factor Authentication (2FA TOTP)
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class TOTPSetupForm(forms.Form):
    """
    Form untuk memasukkan 6 digit token pertama kali saat aktivasi 2FA.
    """

    token = forms.CharField(
        label=_("Kode Verifikasi 6 Digit"),
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "000000",
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "maxlength": "6",
                "autofocus": "autofocus",
                "class": "form-control text-center font-monospace fs-4",
            }
        ),
        help_text=_("Masukkan 6 digit angka dari aplikasi Google Authenticator."),
    )

    def clean_token(self):
        token = self.cleaned_data.get("token", "").strip()
        if not token.isdigit() or len(token) != 6:
            raise forms.ValidationError(_("Kode harus berupa 6 digit angka."))
        return token


class TOTPVerifyForm(forms.Form):
    """
    Form untuk verifikasi 2FA saat login.
    Menerima 6 digit TOTP atau kode cadangan (backup code).
    """

    code = forms.CharField(
        label=_("Kode Authenticator atau Kode Cadangan"),
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Contoh: 123456 atau A1B2-C3D4",
                "autocomplete": "one-time-code",
                "autofocus": "autofocus",
                "class": "form-control text-center",
            }
        ),
        help_text=_(
            "Gunakan 6 digit dari aplikasi autentikator atau salah satu kode cadangan Anda."
        ),
    )

    def clean_code(self):
        code = self.cleaned_data.get("code", "").strip()
        if not code:
            raise forms.ValidationError(_("Kode verifikasi wajib diisi."))
        return code


class TOTPDisableForm(forms.Form):
    """
    Form konfirmasi untuk menonaktifkan 2FA dengan memasukkan password akun.
    """

    password = forms.CharField(
        label=_("Kata Sandi Saat Ini"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Masukkan kata sandi Anda",
                "autocomplete": "current-password",
            }
        ),
        help_text=_("Masukkan kata sandi untuk mengonfirmasi penonaktifan 2FA."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError(_("Kata sandi yang Anda masukkan salah."))
        return password
