"""
Custom User model untuk RDP Starter Kit.
US: US-003 — Custom User model siap pakai

TUJUAN: Extend AbstractUser dengan field custom yang diperlukan project.

ALUR:
  1. Extend AbstractUser untuk tetap pakai built-in authentication
  2. Tambah field custom: email_verified, created_at, updated_at, etc.
  3. Override manager untuk support login dengan email
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    TUJUAN: Custom manager untuk User model dengan email login support.

    ALUR:
      1. Override create_user untuk set email_verified=False
      2. Override create_superuser untuk set email_verified=True otomatis
      3. Support login dengan email atau username
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        TUJUAN: Create regular user dengan email.

        ALUR:
          1. Normalize email address
          2. Hash password
          3. Set email_verified=False by default
          4. Save ke database
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        TUJUAN: Create superuser dengan email dan auto-verify email.

        ALUR:
          1. Set is_staff=True, is_superuser=True
          2. Set email_verified=True (assume admin email terpercaya)
          3. Call create_user
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    TUJUAN: Custom User model untuk RDP dengan email verification dan timestamps.

    ALUR:
      1. Extend AbstractUser (tetap pakai built-in auth)
      2. Tambah email field (unique, untuk login)
      3. Tambah email_verified flag (untuk email verification flow)
      4. Tambah timestamps (created_at, updated_at)

    DIPANGGIL DARI: apps.accounts.models.__init__.py, settings.AUTH_USER_MODEL
    DEPENDENSI: django.contrib.auth.AbstractUser
    """

    # KEPUTUSAN TEKNIS: Email sebagai unique identifier, bukan username
    # ALASAN: Modern apps biasa login dengan email, bukan username
    # ALTERNATIF: Keep username, tapi kurang intuitif
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Unique email address untuk login"),
    )
    email_verified = models.BooleanField(
        _("email verified"),
        default=False,
        help_text=_("Email sudah diverifikasi via link"),
    )
    email_verified_at = models.DateTimeField(
        _("email verified at"),
        null=True,
        blank=True,
        help_text=_("Timestamp saat email diverifikasi"),
    )

    # Timestamps
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )

    # Set email sebagai USERNAME_FIELD dan gunakan UserManager custom
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["email_verified"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        """Return email sebagai string representation."""
        return self.email

    def mark_email_verified(self):
        """
        TUJUAN: Tandai email sebagai verified dan set timestamp.

        ALUR:
          1. Set email_verified=True
          2. Set email_verified_at=now()
          3. Save ke database

        DIPANGGIL DARI: services.user_service.verify_email_token()
        """
        from django.utils import timezone

        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=["email_verified", "email_verified_at"])
