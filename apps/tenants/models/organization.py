"""
Model Organization & OrganizationMember untuk Multi-Tenancy B2B SaaS.
US: US-027 — Multi-Tenancy Subdomain & Context Isolation
"""

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Organization(models.Model):
    """
    Model Organisasi / Tenant utama.
    """

    name = models.CharField("Nama Organisasi", max_length=150)
    slug = models.SlugField("Subdomain / Identifier", max_length=100, unique=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
        verbose_name="Pemilik",
    )
    logo = models.ImageField(
        "Logo Organisasi", upload_to="organization_logos/", blank=True, null=True
    )
    is_active = models.BooleanField("Status Aktif", default=True)
    created_at = models.DateTimeField("Dibuat Pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui Pada", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class OrganizationMember(models.Model):
    """
    Relasi keanggotaan User dalam Organization.
    """

    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Organisasi",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
        verbose_name="Pengguna",
    )
    role = models.CharField("Peran", max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField("Tanggal Bergabung", auto_now_add=True)

    class Meta:
        unique_together = ("organization", "user")
        verbose_name = "Organization Member"
        verbose_name_plural = "Organization Members"

    def __str__(self):
        return f"{self.user} - {self.organization.name} ({self.role})"
