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
from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    # US-004: Register
    path("register/", views.register_wizard, name="register"),
    # US-005: Login
    path("login/", views.user_login, name="login"),
    # US-006: Logout
    path("logout/", views.user_logout, name="logout"),
    # US-008: Verifikasi email
    path("verify-email/resend/", views.resend_verification_view, name="resend_verification"),
    path("verify-email/required/", views.email_verify_required_view, name="verify_required"),
    path("verify-email/<str:token>/", views.verify_email_view, name="verify_email"),
    # US-009: Edit profil & avatar
    path("profile/", views.profile_view, name="profile"),
    path("profile/avatar/", views.avatar_upload_view, name="avatar_upload"),
    # US-007: Lupa password & reset — pakai Django built-in views, custom templates
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/email/password_reset.txt",
            html_email_template_name="accounts/email/password_reset.html",
            subject_template_name="accounts/email/password_reset_subject.txt",
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
