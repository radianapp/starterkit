from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserManagementForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        empty_label="-- Tidak ada Role --",
        label=_("Peran (Role)"),
        widget=forms.Select(attrs={"class": "rdp-form-select"}),
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label=_("Hak Akses Khusus (Permissions)"),
        widget=forms.SelectMultiple(attrs={"class": "rdp-form-select", "style": "height: 150px;"}),
    )

    new_password = forms.CharField(
        label=_("Password Baru"),
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "rdp-form-input", "autocomplete": "new-password"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "rdp-form-input"}),
            "email": forms.EmailInput(attrs={"class": "rdp-form-input"}),
            "first_name": forms.TextInput(attrs={"class": "rdp-form-input"}),
            "last_name": forms.TextInput(attrs={"class": "rdp-form-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "rdp-form-checkbox"}),
        }

    def clean_email(self):
        """
        Validasi domain email saat Admin membuat atau mengedit user.
        """
        from django.conf import settings
        from django.core.exceptions import ValidationError

        email = self.cleaned_data.get("email")
        if email:
            email = email.lower().strip()
            # Validasi domain email
            domain = email.split("@")[1]
            allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", [])
            if allowed_domains and domain not in allowed_domains:
                raise ValidationError(_(f"Domain email @{domain} tidak diizinkan di sistem ini."))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Set initial role to the user's current group if exists
            group = self.instance.groups.first()
            if group:
                self.initial["role"] = group.pk
            # Set initial permissions
            self.initial["user_permissions"] = self.instance.user_permissions.all()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            self._save_role(user)
        return user

    def _save_role(self, user):
        role = self.cleaned_data.get("role")
        user.groups.clear()
        if role:
            user.groups.add(role)

        perms = self.cleaned_data.get("user_permissions")
        if perms is not None:
            user.user_permissions.set(perms)
