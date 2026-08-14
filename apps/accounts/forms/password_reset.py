"""
Form untuk lupa password dengan dukungan CAPTCHA.
US: US-007 ?" Lupa password
"""

from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CaptchaPasswordResetForm(PasswordResetForm):
    """
    TUJUAN: Menambahkan validasi Turnstile CAPTCHA pada form bawaan Django.
    """

    def clean(self):
        cleaned = super().clean()

        # Validasi Cloudflare Turnstile CAPTCHA
        from apps.core.utils.turnstile import verify_turnstile

        # In Django's PasswordResetForm, self.data contains the POST request data
        turnstile_response = self.data.get("cf-turnstile-response")
        if not verify_turnstile(turnstile_response):
            raise ValidationError(
                _("Validasi keamanan (CAPTCHA) gagal. Silakan coba lagi."),
                code="invalid_captcha",
            )

        return cleaned
