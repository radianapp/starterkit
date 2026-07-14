"""
Service layer untuk email verification.
US: US-008 — Verifikasi email

TUJUAN: Generate + validasi token verifikasi email, kirim email verifikasi.
Token pakai django.core.signing — tidak perlu tabel DB tambahan.

ALUR:
  1. generate_verification_token(user) → signed token berisi user_id + salt
  2. send_verification_email(user, request) → kirim email dengan link token
  3. verify_email_token(token) → decode token → return User atau None

DIPANGGIL DARI:
  - apps.accounts.views.register (setelah user dibuat)
  - apps.accounts.views.verify_email (verifikasi link)
  - apps.accounts.views.resend_verification (kirim ulang)

DEPENDENSI: django.core.signing, django.core.mail
"""

from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

User = get_user_model()

# KEPUTUSAN TEKNIS: Token expire 72 jam sesuai AC US-008
# Token berisi user_id saja — data minimal, aman
_SALT = "rdp-email-verification"
_MAX_AGE_SECONDS = 72 * 60 * 60  # 72 jam


def generate_verification_token(user) -> str:
    """
    TUJUAN: Generate signed token untuk verifikasi email.

    ALUR:
      1. Sign user.pk dengan salt khusus email verification
      2. Return token string yang akan dipakai di URL

    DIPANGGIL DARI: send_verification_email()
    """
    return signing.dumps(user.pk, salt=_SALT)


def verify_email_token(token: str):
    """
    TUJUAN: Decode dan validasi token verifikasi email.

    ALUR:
      1. Unsign token dengan max_age=72 jam
      2. Lookup user by pk
      3. Return User atau None jika token expired/invalid/user tidak ada

    DIPANGGIL DARI: apps.accounts.views.verify_email.verify_email_view
    RETURN: (user, error_code) — error_code: None | "expired" | "invalid"
    """
    try:
        user_pk = signing.loads(token, salt=_SALT, max_age=_MAX_AGE_SECONDS)
    except signing.SignatureExpired:
        return None, "expired"
    except signing.BadSignature:
        return None, "invalid"

    try:
        return User.objects.get(pk=user_pk), None
    except User.DoesNotExist:
        return None, "invalid"


def send_verification_email(user, request) -> bool:
    """
    TUJUAN: Kirim email verifikasi ke user baru.

    ALUR:
      1. Generate token
      2. Build absolute verification URL
      3. Render subject + body dari template
      4. Kirim via Django email backend
      5. Return True jika sukses

    DIPANGGIL DARI:
      - apps.accounts.views.register (setelah user dibuat)
      - apps.accounts.views.verify_email.resend_verification_view

    # ⚙️ KONFIGURASI: Email backend via EMAIL_BACKEND di settings
    # Dev: EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # Prod: SMTP via EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, dll.
    """
    token = generate_verification_token(user)
    verify_url = request.build_absolute_uri(
        reverse("accounts:verify_email", kwargs={"token": token})
    )

    subject = render_to_string(
        "accounts/email/verify_email_subject.txt",
        {"user": user},
    ).strip()

    body_txt = render_to_string(
        "accounts/email/verify_email.txt",
        {"user": user, "verify_url": verify_url},
    )

    body_html = render_to_string(
        "accounts/email/verify_email.html",
        {"user": user, "verify_url": verify_url},
    )

    try:
        send_mail(
            subject=subject,
            message=body_txt,
            from_email=None,  # pakai DEFAULT_FROM_EMAIL dari settings
            recipient_list=[user.email],
            html_message=body_html,
            fail_silently=False,
        )
        return True
    except Exception:
        # ⚡ PERFORMA: Log error tapi jangan crash register flow
        import logging

        logging.getLogger(__name__).exception("Gagal kirim email verifikasi ke %s", user.email)
        return False
