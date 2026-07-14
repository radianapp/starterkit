"""
Views untuk accounts app.
"""

from .login import user_login, user_logout
from .profile import avatar_upload_view, profile_view
from .register import register_wizard
from .verify_email import email_verify_required_view, resend_verification_view, verify_email_view

__all__ = [
    "avatar_upload_view",
    "email_verify_required_view",
    "profile_view",
    "register_wizard",
    "resend_verification_view",
    "user_login",
    "user_logout",
    "verify_email_view",
]
