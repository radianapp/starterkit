"""
Forms untuk accounts app.
"""

from .login import LoginForm
from .password_reset import CaptchaPasswordResetForm
from .profile import AvatarForm, ProfileForm
from .register import DynamicStepForm, EmailStepForm, PasswordStepForm
from .totp import TOTPDisableForm, TOTPSetupForm, TOTPVerifyForm

__all__ = [
    "AvatarForm",
    "CaptchaPasswordResetForm",
    "DynamicStepForm",
    "EmailStepForm",
    "LoginForm",
    "PasswordStepForm",
    "ProfileForm",
    "TOTPDisableForm",
    "TOTPSetupForm",
    "TOTPVerifyForm",
]
