"""
Views untuk edit profil user.
US: US-009 — Edit profil & avatar

TUJUAN: Handle GET/POST edit profil dan upload avatar.

ALUR:
  1. profile_view: tampilkan form profil, simpan saat POST
  2. avatar_upload_view: handle upload avatar via HTMX

DIPANGGIL DARI: apps/accounts/urls.py
DEPENDENSI: apps.accounts.forms.profile, apps.accounts.models
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.forms.profile import AvatarForm, ProfileForm


@login_required
def profile_view(request):
    """
    TUJUAN: Tampilkan dan simpan edit profil user (nama + bio).
    US: US-009 — Edit profil & avatar

    ALUR:
      1. GET: inisialisasi form dengan data user saat ini
      2. POST: validasi form → simpan → redirect dengan pesan sukses
      3. POST invalid: re-render form dengan error (HTMX-aware: 422)

    DIPANGGIL DARI: apps/accounts/urls.py → accounts:profile
    DEPENDENSI: ProfileForm, AvatarForm
    """
    user = request.user
    profile = getattr(user, "profile", None)

    avatar_form = AvatarForm()

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save(user)
            messages.success(request, "Profil berhasil diperbarui.")
            if request.headers.get("HX-Request"):
                response = render(
                    request,
                    "accounts/partials/profile_form.html",
                    {
                        "form": form,
                        "avatar_form": avatar_form,
                        "profile": profile,
                        "success": True,
                    },
                )
                response["HX-Trigger"] = "profileUpdated"
                return response
            return redirect("accounts:profile")
        else:
            if request.headers.get("HX-Request"):
                response = render(
                    request,
                    "accounts/partials/profile_form.html",
                    {
                        "form": form,
                        "avatar_form": avatar_form,
                        "profile": profile,
                    },
                )
                response.status_code = 422
                return response
    else:
        # Isi form dengan data user saat ini
        form = ProfileForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": profile.bio if profile else "",
            }
        )

    passkeys = user.passkeys.all()

    from apps.accounts.services.totp_service import is_2fa_enabled, user_has_2fa

    has_2fa = user_has_2fa(user)
    enable_2fa = is_2fa_enabled()
    totp_device = getattr(user, "totp_device", None)
    backup_codes_count = (
        totp_device.backup_codes.filter(is_used=False).count()
        if totp_device and totp_device.is_confirmed
        else 0
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "avatar_form": avatar_form,
            "profile": profile,
            "passkeys": passkeys,
            "has_2fa": has_2fa,
            "enable_2fa": enable_2fa,
            "backup_codes_count": backup_codes_count,
            "page_title": "Edit Profil",
        },
    )


@login_required
def avatar_upload_view(request):
    """
    TUJUAN: Handle upload avatar via HTMX POST.
    US: US-009 — Edit profil & avatar

    ALUR:
      1. Validasi AvatarForm (tipe + ukuran)
      2. Simpan avatar baru ke UserProfile
      3. Return fragment avatar yang terupdate (HTMX swap)
      4. Error: return fragment error dengan status 422

    DIPANGGIL DARI: apps/accounts/urls.py → accounts:avatar_upload
    DEPENDENSI: AvatarForm
    """
    if request.method != "POST":
        return redirect("accounts:profile")

    form = AvatarForm(request.POST, request.FILES)
    profile = getattr(request.user, "profile", None)

    if form.is_valid():
        form.save(request.user)
        # Refresh profile object setelah save
        profile = getattr(request.user, "profile", None)
        messages.success(request, "Foto profil berhasil diperbarui.")
        response = render(
            request,
            "accounts/partials/avatar_preview.html",
            {
                "profile": profile,
                "success": True,
            },
        )
        response["HX-Trigger"] = "avatarUpdated"
        return response

    response = render(
        request,
        "accounts/partials/avatar_upload_form.html",
        {
            "avatar_form": form,
            "profile": profile,
        },
    )
    response.status_code = 422
    return response
