"""
Views untuk Two-Factor Authentication (TOTP / Google Authenticator) dan Backup Codes.
US: US-043 — Two-Factor Authentication (2FA TOTP)

TUJUAN: Mengelola setup 2FA, tampilan recovery codes, penonaktifan 2FA,
        dan verifikasi 2FA saat proses login (2-step authentication).
"""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.accounts.forms.totp import (
    TOTPDisableForm,
    TOTPSetupForm,
    TOTPVerifyForm,
)
from apps.accounts.services.totp_service import (
    confirm_totp_device,
    disable_totp_for_user,
    get_or_create_pending_device,
    is_2fa_enabled,
    user_has_2fa,
    verify_user_totp,
)

User = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def totp_setup_view(request):
    """
    TUJUAN: Setup 2FA baru bagi user yang sudah login.
    ALUR:
      1. GET: Generate pending TOTPDevice, buat QR code & secret Base32.
      2. POST: Validasi 6 digit kode dari aplikasi authenticator.
      3. Sukses: Konfirmasi device, generate 8 backup codes, simpan di session, redirect ke halaman backup codes.
    """
    if not is_2fa_enabled():
        messages.error(
            request, "Fitur Two-Factor Authentication saat ini dinonaktifkan oleh sistem."
        )
        return redirect("accounts:profile")

    device, otp_uri, qr_data_uri = get_or_create_pending_device(request.user)
    is_htmx = request.headers.get("HX-Request") == "true"

    if request.method == "POST":
        form = TOTPSetupForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]
            success, backup_codes = confirm_totp_device(request.user, token)
            if success:
                request.session["recent_backup_codes"] = backup_codes
                messages.success(request, "Two-Factor Authentication berhasil diaktifkan.")
                backup_codes_url = reverse("accounts:2fa_backup_codes")
                if is_htmx:
                    response = HttpResponse()
                    response["HX-Redirect"] = backup_codes_url
                    return response
                return redirect("accounts:2fa_backup_codes")
            else:
                form.add_error(
                    "token",
                    "Kode verifikasi salah atau sudah kadaluarsa. Pastikan jam pada HP Anda akurat.",
                )

        ctx = {
            "form": form,
            "secret_key": device.secret_key,
            "qr_data_uri": qr_data_uri,
            "otp_uri": otp_uri,
            "page_title": "Setup Two-Factor Authentication (2FA)",
        }
        template = "accounts/partials/2fa_setup_form.html" if is_htmx else "accounts/2fa_setup.html"
        return render(request, template, ctx, status=422)

    form = TOTPSetupForm()
    return render(
        request,
        "accounts/2fa_setup.html",
        {
            "form": form,
            "secret_key": device.secret_key,
            "qr_data_uri": qr_data_uri,
            "otp_uri": otp_uri,
            "page_title": "Setup Two-Factor Authentication (2FA)",
        },
    )


@login_required
@require_http_methods(["GET"])
def totp_backup_codes_view(request):
    """
    TUJUAN: Menampilkan backup / recovery codes yang baru di-generate.
    Hanya ditampilkan sekali setelah aktivasi.
    """
    backup_codes = request.session.pop("recent_backup_codes", None)
    if not backup_codes:
        # Jika session sudah tidak ada, arahkan kembali ke profile
        return redirect("accounts:profile")

    return render(
        request,
        "accounts/2fa_backup_codes.html",
        {
            "backup_codes": backup_codes,
            "page_title": "Kode Cadangan (Recovery Codes) 2FA",
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def totp_disable_view(request):
    """
    TUJUAN: Menonaktifkan 2FA dengan konfirmasi kata sandi.
    """
    if not is_2fa_enabled():
        return redirect("accounts:profile")

    if not user_has_2fa(request.user):
        messages.info(request, "Akun Anda belum mengaktifkan Two-Factor Authentication.")
        return redirect("accounts:profile")

    is_htmx = request.headers.get("HX-Request") == "true"

    if request.method == "POST":
        form = TOTPDisableForm(request.user, request.POST)
        if form.is_valid():
            disable_totp_for_user(request.user)
            messages.success(request, "Two-Factor Authentication berhasil dinonaktifkan.")
            profile_url = reverse("accounts:profile")
            if is_htmx:
                response = HttpResponse()
                response["HX-Redirect"] = profile_url
                return response
            return redirect("accounts:profile")

        ctx = {
            "form": form,
            "page_title": "Nonaktifkan Two-Factor Authentication (2FA)",
        }
        template = (
            "accounts/partials/2fa_disable_form.html" if is_htmx else "accounts/2fa_disable.html"
        )
        return render(request, template, ctx, status=422)

    form = TOTPDisableForm(request.user)
    return render(
        request,
        "accounts/2fa_disable.html",
        {
            "form": form,
            "page_title": "Nonaktifkan Two-Factor Authentication (2FA)",
        },
    )


@require_http_methods(["GET", "POST"])
def totp_verify_login_view(request):
    """
    TUJUAN: Verifikasi 2FA langkah ke-2 pada saat login.
    ALUR:
      1. Periksa apakah session memiliki `pre_2fa_user_id`.
      2. GET: Render form verifikasi 2FA (TOTP atau Backup Code).
      3. POST: Validasi kode. Jika benar -> auth_login() dan redirect ke next.
    """
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("accounts:login")

    user = User.objects.filter(pk=user_id, is_active=True).first()
    if not user:
        request.session.pop("pre_2fa_user_id", None)
        return redirect("accounts:login")

    next_url = request.session.get("pre_2fa_next") or "/"
    is_htmx = request.headers.get("HX-Request") == "true"

    if request.method == "POST":
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if verify_user_totp(user, code):
                # Login sukses
                remember_me = request.session.get("pre_2fa_remember_me", False)

                # Hapus session sementara
                request.session.pop("pre_2fa_user_id", None)
                request.session.pop("pre_2fa_remember_me", None)
                request.session.pop("pre_2fa_next", None)

                if not remember_me:
                    request.session.set_expiry(0)

                auth_login(request, user, backend="apps.accounts.backends.EmailOrUsernameBackend")
                messages.success(request, "Autentikasi dua faktor berhasil. Selamat datang!")

                if is_htmx:
                    response = render(request, "accounts/partials/login_success.html", {})
                    response["HX-Redirect"] = next_url
                    return response
                return redirect(next_url)
            else:
                form.add_error("code", "Kode verifikasi atau kode cadangan tidak valid.")

        ctx = {
            "form": form,
            "user_email": user.email,
            "next": next_url,
            "page_title": "Verifikasi Two-Factor Authentication",
        }
        template = (
            "accounts/partials/2fa_verify_form.html" if is_htmx else "accounts/2fa_verify.html"
        )
        return render(request, template, ctx, status=422)

    form = TOTPVerifyForm()
    return render(
        request,
        "accounts/2fa_verify.html",
        {
            "form": form,
            "user_email": user.email,
            "next": next_url,
            "page_title": "Verifikasi Two-Factor Authentication",
        },
    )
