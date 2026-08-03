"""
URL configuration untuk accounts app.
US: US-004, US-005, US-006, US-007, US-008, US-009

TUJUAN: Route semua auth-related URLs.

ALUR:
  1. Setup login, register, logout, forgot-password, reset-password, profile, dll.
  2. Gunakan app_name="accounts" untuk reverse URL dengan namespace
  3. Setup path() untuk setiap view
"""

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.accounts import views
from apps.accounts.forms import CaptchaPasswordResetForm

app_name = "accounts"

urlpatterns = [
    # US-004: Register
    path("register/", views.register_wizard, name="register"),
    # US-005: Login
    path("login/", views.user_login, name="login"),
    # US-006: Logout
    path("logout/", views.user_logout, name="logout"),
    # Ganti password paksa untuk user baru
    path("force-password-change/", views.ForcePasswordChangeView.as_view(), name="force_password_change"),
    # US-008: Verifikasi email
    path("verify-email/resend/", views.resend_verification_view, name="resend_verification"),
    path("verify-email/required/", views.email_verify_required_view, name="verify_required"),
    path("verify-email/<str:token>/", views.verify_email_view, name="verify_email"),
    # US-009: Edit profil & avatar
    path("profile/", views.profile_view, name="profile"),
    path("profile/avatar/", views.avatar_upload_view, name="avatar_upload"),
    
    # Settings Global
    path("settings/", views.SettingsView.as_view(), name="settings"),
    
    # Manajemen Pengguna (SuperAdmin)
    path("users/", views.user_list, name="user_list"),
    path("users/partial/", views.user_list_partial, name="user_list_partial"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path("users/bulk-upload/", views.user_bulk_upload, name="user_bulk_upload"),
    path("users/<int:user_id>/resend-invite/", views.resend_invite_email, name="resend_invite_email"),
    
    # WebAuthn (Passkeys)
    path("webauthn/register/challenge/", views.register_challenge, name="webauthn_register_challenge"),
    path("webauthn/register/verify/", views.register_verify, name="webauthn_register_verify"),
    path("webauthn/login/challenge/", views.login_challenge, name="webauthn_login_challenge"),
    path("webauthn/login/verify/", views.login_verify, name="webauthn_login_verify"),
    path("webauthn/passkey/<int:pk>/delete/", views.delete_passkey, name="webauthn_delete_passkey"),
    
    # US-007: Lupa password & reset — pakai Django built-in views, custom templates
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            form_class=CaptchaPasswordResetForm,
            email_template_name="accounts/email/password_reset.txt",
            html_email_template_name="accounts/email/password_reset.html",
            subject_template_name="accounts/email/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
            extra_context={"title": "Lupa Password"},
        ),
        name="password_reset",
    ),
    path(
        "password-reset/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
            extra_context={"title": "Buat Password Baru"},
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
