"""
Service untuk autentikasi menggunakan WebAuthn (Passkeys / Biometrik).
"""

from typing import Dict, Any, Tuple, Optional
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.structs import (
    RegistrationCredential,
    AuthenticationCredential,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)
from webauthn.helpers.exceptions import InvalidRegistrationResponse, InvalidAuthenticationResponse

from apps.accounts.models import PasskeyCredential

User = get_user_model()


def get_rp_id(request) -> str:
    """Mengambil RP ID (domain name) dari request."""
    return request.get_host().split(":")[0]


def get_origin(request) -> str:
    """Mengambil Origin dari request."""
    scheme = request.scheme
    host = request.get_host()
    return f"{scheme}://{host}"


def generate_registration_challenge(request, user) -> Tuple[Dict[str, Any], str]:
    """
    Menghasilkan opsi pendaftaran (challenge) untuk diteruskan ke navigator.credentials.create()
    Kembalian: (options_dict, challenge_b64)
    """
    rp_id = get_rp_id(request)
    rp_name = getattr(settings, "SITE_NAME", "RDP Starter Kit")

    # Ambil kredensial yang sudah ada (exclude dari pendaftaran agar tidak dobel)
    existing_credentials = PasskeyCredential.objects.filter(user=user)
    exclude_credentials = []
    for cred in existing_credentials:
        exclude_credentials.append(
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(cred.credential_id))
        )

    options = generate_registration_options(
        rp_id=rp_id,
        rp_name=rp_name,
        user_id=str(user.id).encode("utf-8"),
        user_name=user.email,
        user_display_name=user.get_full_name() or user.email,
        exclude_credentials=exclude_credentials,
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
    )

    options_json = json.loads(options_to_json(options))
    # Simpan challenge di session
    request.session["webauthn_registration_challenge"] = options_json["challenge"]

    return options_json


from webauthn.helpers import bytes_to_base64url

def verify_and_save_registration(request, user, response_data: Dict[str, Any], device_name: str) -> PasskeyCredential:
    """
    Memverifikasi respons pendaftaran dari browser dan menyimpannya ke database.
    """
    challenge = request.session.get("webauthn_registration_challenge")
    if not challenge:
        raise ValueError("Tantangan (challenge) pendaftaran tidak ditemukan atau sudah kadaluarsa.")

    rp_id = get_rp_id(request)
    origin = get_origin(request)

    try:
        credential = RegistrationCredential.parse_raw(json.dumps(response_data))
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=challenge.encode("utf-8"),
            expected_origin=origin,
            expected_rp_id=rp_id,
            require_user_verification=False,
        )
    except Exception as e:
        raise ValueError(f"Verifikasi kredensial gagal: {str(e)}")

    # Simpan ke DB
    passkey = PasskeyCredential.objects.create(
        user=user,
        name=device_name or "Passkey Device",
        credential_id=bytes_to_base64url(verification.credential_id) if isinstance(verification.credential_id, bytes) else verification.credential_id,
        public_key=bytes_to_base64url(verification.credential_public_key) if isinstance(verification.credential_public_key, bytes) else verification.credential_public_key,
        sign_count=verification.sign_count,
    )

    # Bersihkan session
    del request.session["webauthn_registration_challenge"]

    return passkey


def generate_authentication_challenge(request) -> Dict[str, Any]:
    """
    Menghasilkan opsi autentikasi untuk diteruskan ke navigator.credentials.get()
    Catatan: Tidak memasukkan list allowed_credentials agar user bisa memilih passkey mana saja.
    """
    rp_id = get_rp_id(request)

    options = generate_authentication_options(
        rp_id=rp_id,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    options_json = json.loads(options_to_json(options))
    request.session["webauthn_authentication_challenge"] = options_json["challenge"]

    return options_json


def verify_authentication(request, response_data: Dict[str, Any]) -> User:
    """
    Memverifikasi respons login dari browser dan mengembalikan user yang cocok.
    """
    challenge = request.session.get("webauthn_authentication_challenge")
    if not challenge:
        raise ValueError("Tantangan (challenge) autentikasi tidak ditemukan atau sudah kadaluarsa.")

    rp_id = get_rp_id(request)
    origin = get_origin(request)

    try:
        credential = AuthenticationCredential.parse_raw(json.dumps(response_data))
    except Exception as e:
        raise ValueError(f"Format kredensial tidak valid: {str(e)}")

    # Cari kredensial di DB berdasarkan ID
    try:
        # credential.id pada model AuthenticationCredential biasanya base64url string
        passkey = PasskeyCredential.objects.get(credential_id=credential.id)
    except PasskeyCredential.DoesNotExist:
        raise ValueError("Kredensial tidak ditemukan atau belum terdaftar.")

    try:
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=challenge.encode("utf-8"),
            expected_origin=origin,
            expected_rp_id=rp_id,
            credential_public_key=base64url_to_bytes(passkey.public_key) if isinstance(passkey.public_key, str) else passkey.public_key,
            credential_current_sign_count=passkey.sign_count,
            require_user_verification=False,
        )
    except Exception as e:
        raise ValueError(f"Verifikasi autentikasi gagal: {str(e)}")

    # Update sign count
    passkey.sign_count = verification.new_sign_count
    from django.utils import timezone
    passkey.last_used_at = timezone.now()
    passkey.save(update_fields=["sign_count", "last_used_at"])

    # Bersihkan session
    del request.session["webauthn_authentication_challenge"]

    return passkey.user
