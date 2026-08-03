"""
Adapter kustom untuk django-allauth.
US: US-004 — Register akun baru

TUJUAN: Menerapkan batasan bisnis (seperti whitelist domain email)
saat user mendaftar, baik melalui form standar allauth maupun lewat SSO (Google).
"""

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DomainRestrictAdapter(DefaultAccountAdapter):
    """
    Adapter kustom untuk memastikan hanya email dari domain tertentu
    yang diizinkan mendaftar.
    """

    def clean_email(self, email):
        """
        Validasi email sebelum akun dibuat.
        Berlaku untuk pendaftaran manual (jika pakai allauth) maupun SSO (Google).
        """
        # Biarkan adapter default menyanitasi email terlebih dahulu
        email = super().clean_email(email)

        # Ekstrak bagian domain dari email
        domain = email.split("@")[1].lower()

        # Ambil daftar domain dari settings (dikonfigurasi via .env)
        allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])

        # Jika ada batasan (list tidak kosong) dan domain tidak terdaftar
        if allowed_domains and domain not in allowed_domains:
            raise ValidationError(
                _(
                    f"Pendaftaran ditolak: Domain email @{domain} tidak memiliki akses. "
                    f"Harap gunakan email perusahaan yang sah."
                )
            )

        return email
