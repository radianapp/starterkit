"""
Form untuk edit profil user.
US: US-009 — Edit profil & avatar

TUJUAN: Validasi update nama, bio, dan avatar upload.

ALUR:
  1. ProfileForm: ubah first_name, last_name (dari User) + bio (dari UserProfile)
  2. AvatarForm: upload file avatar dengan validasi tipe + ukuran

DIPANGGIL DARI: apps.accounts.views.profile
"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import UserProfile

User = get_user_model()

_MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2MB
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


class ProfileForm(forms.Form):
    """
    TUJUAN: Form edit nama dan bio profil.
    US: US-009 — Edit profil & avatar

    ALUR:
      1. Ambil first_name, last_name dari User
      2. Ambil bio dari UserProfile
      3. Validasi dan simpan keduanya

    DIPANGGIL DARI: apps.accounts.views.profile.profile_view
    """

    first_name = forms.CharField(
        label=_("Nama Depan"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nama depan"}),
    )
    last_name = forms.CharField(
        label=_("Nama Belakang"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nama belakang"}),
    )
    bio = forms.CharField(
        label=_("Bio"),
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Cerita singkat tentang kamu..."}),
    )

    def save(self, user):
        """
        TUJUAN: Simpan data profil ke User dan UserProfile.

        ALUR:
          1. Update User.first_name dan User.last_name
          2. Update UserProfile.bio
          3. Save keduanya

        DIPANGGIL DARI: apps.accounts.views.profile.profile_view
        """
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save(update_fields=["first_name", "last_name"])

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.bio = self.cleaned_data["bio"]
        profile.save(update_fields=["bio"])

        return user


class AvatarForm(forms.Form):
    """
    TUJUAN: Form upload avatar dengan validasi tipe file dan ukuran.
    US: US-009 — Edit profil & avatar

    ALUR:
      1. Validasi tipe MIME: hanya JPG, PNG, WebP
      2. Validasi ukuran: maks 2MB
      3. Simpan ke UserProfile.avatar

    DIPANGGIL DARI: apps.accounts.views.profile.avatar_upload_view
    """

    avatar = forms.ImageField(
        label=_("Foto Profil"),
        help_text=_("JPG, PNG, atau WebP. Maksimal 2MB."),
    )

    def clean_avatar(self):
        """Validasi tipe dan ukuran file."""
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return avatar

        if avatar.size > _MAX_AVATAR_SIZE:
            raise ValidationError(
                _("Ukuran file terlalu besar. Maksimal 2MB."),
            )

        content_type = getattr(avatar, "content_type", "")
        if content_type and content_type not in _ALLOWED_IMAGE_TYPES:
            raise ValidationError(
                _("Format tidak didukung. Gunakan JPG, PNG, atau WebP."),
            )

        return avatar

    def save(self, user):
        """
        TUJUAN: Simpan avatar ke UserProfile.

        ALUR:
          1. Hapus avatar lama jika ada (cegah storage leak)
          2. Simpan avatar baru

        DIPANGGIL DARI: apps.accounts.views.profile.avatar_upload_view
        """
        avatar_file = self.cleaned_data["avatar"]
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Hapus file lama sebelum ganti
        if profile.avatar:
            profile.avatar.delete(save=False)

        profile.avatar = avatar_file
        profile.save(update_fields=["avatar"])
        return profile
