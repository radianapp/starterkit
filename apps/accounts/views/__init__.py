"""
Views untuk accounts app.
"""

from .login import user_login, user_logout
from .password import ForcePasswordChangeView
from .profile import avatar_upload_view, profile_view
from .register import register_wizard
from .settings import SettingsView
from .users import (
    resend_invite_email,
    user_add,
    user_bulk_upload,
    user_edit,
    user_list,
    user_list_partial,
)
from .verify_email import email_verify_required_view, resend_verification_view, verify_email_view
from .webauthn import (
    delete_passkey,
    login_challenge,
    login_verify,
    register_challenge,
    register_verify,
)

__all__ = [
    "ForcePasswordChangeView",
    "SettingsView",
    "avatar_upload_view",
    "delete_passkey",
    "email_verify_required_view",
    "login_challenge",
    "login_verify",
    "profile_view",
    "register_challenge",
    "register_verify",
    "register_wizard",
    "resend_invite_email",
    "resend_verification_view",
    "user_add",
    "user_bulk_upload",
    "user_edit",
    "user_list",
    "user_list_partial",
    "user_login",
    "user_logout",
    "verify_email_view",
]
