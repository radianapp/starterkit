"""
Service layer untuk Two-Factor Authentication (TOTP / Google Authenticator) dan Backup Codes.
US: US-043 — Two-Factor Authentication (2FA TOTP)

TUJUAN: Menyediakan fungsi manajemen secret TOTP, generate QR Code, verifikasi token OTP,
        pembuatan dan konsumsi kode pemulihan cadangan (backup codes).
"""

import base64
import io
import secrets

import pyotp
import qrcode
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from qrcode.image.pil import PilImage

from apps.accounts.models.totp import TOTPBackupCode, TOTPDevice


def is_2fa_enabled() -> bool:
    """Cek apakah fitur 2FA diaktifkan secara global di settings."""
    return getattr(settings, "ENABLE_2FA", True)


def user_has_2fa(user) -> bool:
    """Cek apakah user memiliki perangkat TOTP yang aktif dan terkonfirmasi."""
    if not is_2fa_enabled():
        return False
    if not user or not user.is_authenticated:
        return False
    return TOTPDevice.objects.filter(user=user, is_confirmed=True).exists()


def generate_totp_secret() -> str:
    """Generate random Base32 secret string untuk TOTP."""
    return pyotp.random_base32()


def get_totp_uri(user, secret_key: str, issuer_name: str | None = None) -> str:
    """
    Buat URI standar otpauth:// untuk QR code Google Authenticator.
    Format: otpauth://totp/Issuer:user@email.com?secret=...&issuer=Issuer
    """
    if issuer_name is None:
        issuer_name = getattr(settings, "SITE_NAME", "RDP Starter Kit")
    totp = pyotp.TOTP(secret_key)
    return totp.provisioning_uri(name=user.email, issuer_name=issuer_name)


def generate_qr_code_data_uri(otp_uri: str) -> str:
    """
    Render string OTP URI menjadi gambar QR Code dalam format Data URI (PNG base64).
    Dapat langsung dirender di tag <img src="data:image/png;base64,...">.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_img}"


def get_or_create_pending_device(user) -> tuple[TOTPDevice, str, str]:
    """
    Ambil atau buat TOTPDevice dalam status pending (is_confirmed=False).
    Mengembalikan (device, otp_uri, qr_data_uri).
    """
    device = TOTPDevice.objects.filter(user=user).first()
    if not device:
        secret = generate_totp_secret()
        device = TOTPDevice.objects.create(
            user=user,
            secret_key=secret,
            is_confirmed=False,
        )
    elif device.is_confirmed:
        # Jika sudah confirmed tapi minta setup lagi, buat secret baru
        device.secret_key = generate_totp_secret()
        device.is_confirmed = False
        device.save(update_fields=["secret_key", "is_confirmed"])

    otp_uri = get_totp_uri(user, device.secret_key)
    qr_data_uri = generate_qr_code_data_uri(otp_uri)
    return device, otp_uri, qr_data_uri


def generate_backup_codes(device: TOTPDevice, count: int = 8) -> list[str]:
    """
    Hapus backup codes lama dan buat `count` buah backup code baru.
    Simpan hash-nya di database dan kembalikan daftar kode plain text (hanya untuk user).
    """
    device.backup_codes.all().delete()

    plain_codes = []
    backup_code_objects = []

    for _ in range(count):
        # Format: xxxx-xxxx (8 karakter acak)
        part1 = secrets.token_hex(2).upper()
        part2 = secrets.token_hex(2).upper()
        raw_code = f"{part1}-{part2}"
        plain_codes.append(raw_code)

        backup_code_objects.append(
            TOTPBackupCode(
                device=device,
                code_hash=make_password(raw_code.replace("-", "").strip()),
                is_used=False,
            )
        )

    TOTPBackupCode.objects.bulk_create(backup_code_objects)
    return plain_codes


def confirm_totp_device(user, code: str) -> tuple[bool, list[str]]:
    """
    Verifikasi kode awal saat aktivasi 2FA.
    Jika valid, ubah is_confirmed=True dan generate backup codes.
    Mengembalikan (is_valid, list_of_plain_backup_codes).
    """
    device = TOTPDevice.objects.filter(user=user, is_confirmed=False).first()
    if not device:
        return False, []

    clean_code = str(code).strip().replace(" ", "")
    totp = pyotp.TOTP(device.secret_key)
    if totp.verify(clean_code, valid_window=1):
        device.is_confirmed = True
        device.last_used_at = timezone.now()
        device.save(update_fields=["is_confirmed", "last_used_at"])

        # Buat backup codes
        backup_codes = generate_backup_codes(device)
        return True, backup_codes

    return False, []


def verify_and_consume_backup_code(device: TOTPDevice, raw_code: str) -> bool:
    """
    Periksa apakah raw_code cocok dengan salah satu backup code yang belum dipakai.
    Jika cocok, tandai is_used=True dan simpan waktu penggunaan.
    """
    clean_code = str(raw_code).strip().replace("-", "").replace(" ", "").upper()
    if not clean_code:
        return False

    unused_codes = device.backup_codes.filter(is_used=False)
    for backup_code in unused_codes:
        if check_password(clean_code, backup_code.code_hash):
            backup_code.is_used = True
            backup_code.used_at = timezone.now()
            backup_code.save(update_fields=["is_used", "used_at"])
            return True

    return False


def verify_user_totp(user, code_or_backup: str) -> bool:
    """
    Verifikasi kode TOTP (6 digit) atau Backup Code saat login / aksi sensitif.
    """
    if not user or not user.is_authenticated:
        # Jika dipanggil pada alur pre-login (user instance didapat dari backend)
        pass

    try:
        device = user.totp_device
    except (TOTPDevice.DoesNotExist, AttributeError):
        return False

    if not device.is_confirmed:
        return False

    clean_input = str(code_or_backup).strip().replace(" ", "")

    # Cek apakah 6-digit TOTP
    if clean_input.isdigit() and len(clean_input) == 6:
        totp = pyotp.TOTP(device.secret_key)
        if totp.verify(clean_input, valid_window=1):
            device.last_used_at = timezone.now()
            device.save(update_fields=["last_used_at"])
            return True

    # Cek apakah Backup Code
    return verify_and_consume_backup_code(device, clean_input)


def disable_totp_for_user(user) -> bool:
    """
    Nonaktifkan 2FA dengan menghapus TOTPDevice (cascade menghapus backup codes).
    """
    count, _ = TOTPDevice.objects.filter(user=user).delete()
    return count > 0
