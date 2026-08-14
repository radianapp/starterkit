"""
TenantModelMixin: Mixin untuk Model yang memiliki isolasi data per Organisasi.
"""

from django.db import models


class TenantQuerySet(models.QuerySet):
    def for_tenant(self, tenant):
        if tenant is None:
            return self
        return self.filter(organization=tenant)


class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_tenant(self, tenant):
        return self.get_queryset().for_tenant(tenant)


class TenantModelMixin(models.Model):
    """
    Abstract Model Mixin yang menambahkan FK ke Organization dan manager for_tenant.
    """

    organization = models.ForeignKey(
        "tenants.Organization",
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        verbose_name="Organisasi/Tenant",
        null=True,
        blank=True,
    )

    objects = TenantManager()

    class Meta:
        abstract = True
