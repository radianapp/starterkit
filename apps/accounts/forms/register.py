"""
Forms untuk registration wizard.
US: US-004 — Register akun baru

TUJUAN: Form per step wizard — email, dynamic questions, password.

ALUR:
  1. EmailStepForm — validasi email unik
  2. DynamicStepForm — generate field dari definisi step (REGISTRATION_STEPS)
  3. PasswordStepForm — password + konfirmasi
"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class EmailStepForm(forms.Form):
    """
    TUJUAN: Step 0 wizard — kumpulkan email dan validasi keunikannya.

    ALUR:
      1. Input email
      2. Validasi format email
      3. Cek apakah email sudah dipakai user lain

    DIPANGGIL DARI: apps.accounts.views.register.register_wizard
    """

    email = forms.EmailField(
        label=_("Alamat Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}),
    )

    def clean_email(self):
        """
        TUJUAN: Validasi email belum dipakai user lain dan domain diizinkan.
        """
        from django.conf import settings

        email = self.cleaned_data["email"].lower().strip()

        # Validasi domain email
        domain = email.split("@")[1]
        allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])
        if allowed_domains and domain not in allowed_domains:
            raise ValidationError(
                _(
                    f"Pendaftaran ditolak: Domain email @{domain} tidak memiliki akses. "
                    f"Harap gunakan email perusahaan yang sah."
                )
            )

        # Validasi keunikan email
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("Email ini sudah terdaftar. Silakan login atau gunakan email lain.")
            )
        return email

    def clean(self):
        """Validasi Cloudflare Turnstile CAPTCHA"""
        cleaned = super().clean()
        from apps.core.utils.turnstile import verify_turnstile

        turnstile_response = self.data.get("cf-turnstile-response")

        if not verify_turnstile(turnstile_response):
            raise ValidationError(_("Validasi keamanan (CAPTCHA) gagal. Silakan coba lagi."))

        return cleaned


class DynamicStepForm(forms.Form):
    """
    TUJUAN: Generate form field dari definisi step di REGISTRATION_STEPS.

    ALUR:
      1. Terima step_def dict: {key, label, type, required, choices (optional)}
      2. Generate field sesuai type
      3. Validasi required

    DIPANGGIL DARI: apps.accounts.views.register.register_wizard
    DEPENDENSI: settings.REGISTRATION_STEPS
    """

    def __init__(self, step_def: dict, *args, **kwargs):
        """
        TUJUAN: Inisialisasi form dengan satu field dari step_def.

        ALUR:
          1. Panggil super().__init__()
          2. Tambah satu field sesuai type di step_def
        """
        super().__init__(*args, **kwargs)
        key = step_def["key"]
        label = step_def["label"]
        required = step_def.get("required", True)
        field_type = step_def.get("type", "text")

        if field_type == "select":
            choices = [("", f"-- Pilih {label} --")] + [(c, c) for c in step_def.get("choices", [])]
            self.fields[key] = forms.ChoiceField(
                label=label,
                choices=choices,
                required=required,
            )
        elif field_type == "textarea":
            self.fields[key] = forms.CharField(
                label=label,
                required=required,
                widget=forms.Textarea(attrs={"rows": 3}),
            )
        elif field_type == "email":
            self.fields[key] = forms.EmailField(label=label, required=required)
        else:
            # default: text
            self.fields[key] = forms.CharField(label=label, required=required)


class PasswordStepForm(forms.Form):
    """
    TUJUAN: Step terakhir wizard — input password dan konfirmasi.

    ALUR:
      1. Input password (min 8 karakter)
      2. Input konfirmasi password
      3. Validasi keduanya cocok

    DIPANGGIL DARI: apps.accounts.views.register.register_wizard
    """

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
        help_text=_("Minimal 8 karakter."),
    )
    password2 = forms.CharField(
        label=_("Konfirmasi Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        """
        TUJUAN: Validasi password1 dan password2 cocok.
        """
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError({"password2": _("Password tidak cocok.")})
        return cleaned
