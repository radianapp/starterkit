"""
Views untuk email verification flow.
US: US-008 — Verifikasi email

TUJUAN: Handle klik link verifikasi, resend, dan halaman "cek email kamu".

ALUR:
  - verify_email_view: klik link → validasi token → mark verified → redirect dashboard
  - resend_verification_view: POST → kirim ulang email → feedback
  - email_verify_required_view: halaman prompt "cek email" untuk user belum verify

DIPANGGIL DARI: apps/accounts/urls.py
DEPENDENSI: apps.accounts.services.email_service
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.services.email_service import send_verification_email, verify_email_token


def verify_email_view(request, token: str):
    """
    TUJUAN: Proses klik link verifikasi email.
    US: US-008 — Verifikasi email

    ALUR:
      1. Decode token → user
      2. Jika expired → tampil halaman expired + opsi resend
      3. Jika invalid → tampil error
      4. Jika sudah verified → redirect dashboard (idempotent)
      5. Jika valid → mark_email_verified() → redirect dashboard
    """
    user, error = verify_email_token(token)

    if error == "expired":
        return render(request, "accounts/verify_email_expired.html", {"token": token})

    if error == "invalid" or user is None:
        return render(request, "accounts/verify_email_invalid.html", {})

    # Idempotent — sudah verified sebelumnya tetap OK
    if not user.email_verified:
        user.mark_email_verified()

    messages.success(request, "Email berhasil diverifikasi. Selamat datang!")
    return redirect("dashboard:index")


@login_required
def resend_verification_view(request):
    """
    TUJUAN: Kirim ulang email verifikasi ke user yang sedang login.
    US: US-008 — Verifikasi email

    ALUR:
      1. Cek user belum verified
      2. Kirim email → feedback sukses atau error
      3. Redirect ke halaman verify_required
    """
    user = request.user

    if user.email_verified:
        messages.info(request, "Email kamu sudah terverifikasi.")
        return redirect("dashboard:index")

    sent = send_verification_email(user, request)
    if sent:
        messages.success(request, f"Email verifikasi sudah dikirim ke {user.email}.")
    else:
        messages.error(request, "Gagal mengirim email. Coba lagi beberapa saat.")

    return redirect("accounts:verify_required")


@login_required
def email_verify_required_view(request):
    """
    TUJUAN: Halaman prompt "cek email kamu" untuk user yang belum verifikasi.
    US: US-008 — Verifikasi email

    ALUR:
      1. Jika sudah verified → redirect dashboard
      2. Render halaman dengan info email dan tombol resend
    """
    if request.user.email_verified:
        return redirect("dashboard:index")

    return render(request, "accounts/verify_email_required.html", {"user": request.user})
