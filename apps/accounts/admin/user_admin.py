"""
Admin configuration untuk User dan UserProfile models.
US: US-012 — Admin Django kustom
US: US-003 — Custom User model siap pakai

TUJUAN: Setup admin panel untuk manage users dan profiles dengan interface yang user-friendly.

ALUR:
  1. Register User model dengan custom UserAdmin
  2. Register UserProfile model dengan custom UserProfileAdmin
  3. Setup search, filter, list display, readonly fields
  4. Setup inlines untuk edit profile dalam User admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    """
    TUJUAN: Inline admin untuk edit UserProfile dalam User admin.

    ALUR:
      1. Display avatar, bio
      2. Allow edit profile fields dalam User admin page (OneToOne)
      3. Extra=0 karena OneToOne — hanya 1 profile per user
    """

    model = UserProfile
    extra = 0
    fields = ("avatar", "bio", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    TUJUAN: Custom admin interface untuk User model.

    ALUR:
      1. Override fieldsets untuk include email_verified dan timestamps
      2. Setup search_fields untuk cari email dan nama
      3. Setup list_filter untuk filter by email_verified dan created_at
      4. Include UserProfileInline untuk edit profile inline
      5. Setup list_display dengan kolom penting

    DIPANGGIL DARI: Django admin site
    DEPENDENSI: Django auth admin
    """

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "username")},
        ),
        (
            _("Email Verification"),
            {
                "fields": ("email_verified", "email_verified_at"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "created_at", "updated_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "email_verified",
        "created_at",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "email_verified",
        "created_at",
    )
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "last_login")

    def get_inlines(self, request, obj=None):
        """Return inlines list for this admin."""
        return [UserProfileInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    TUJUAN: Admin interface untuk UserProfile model.

    ALUR:
      1. Display user, avatar, bio
      2. Setup search untuk cari user by email
      3. Setup list_filter untuk filter by created_at
      4. Readonly untuk timestamps dan user field

    DIPANGGIL DARI: Django admin site
    DEPENDENSI: UserProfile model
    """

    list_display = ("user", "avatar", "bio", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    readonly_fields = ("user", "created_at", "updated_at")
    fields = ("user", "avatar", "bio", "created_at", "updated_at")
    ordering = ("-created_at",)
