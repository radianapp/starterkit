"""
Form untuk Bulk Upload Users.
US: US-002 — Manajemen Pengguna
"""

from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class BulkUploadForm(forms.Form):
    """
    TUJUAN: Menangani validasi input file CSV dari SuperAdmin.
    """
    csv_file = forms.FileField(
        label=_("File CSV"),
        help_text=_("Pilih file CSV yang berisi data pengguna. Kolom wajib: email. Kolom opsional: first_name, last_name. Kolom lainnya akan disimpan sebagai custom field."),
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        widget=forms.FileInput(attrs={
            "accept": ".csv",
            "class": "file-input"
        })
    )
