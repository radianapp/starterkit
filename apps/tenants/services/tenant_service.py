"""
Service layer untuk logika bisnis Organisasi / Multi-Tenancy.
"""

from apps.tenants.models import Organization, OrganizationMember


def get_user_organizations(user):
    """Mengambil daftar organisasi tempat user bergabung."""
    if not user.is_authenticated:
        return Organization.objects.none()
    return Organization.objects.filter(members__user=user, is_active=True).distinct()


def switch_active_tenant(request, organization_id):
    """Mengubah organisasi aktif pada session user."""
    if not request.user.is_authenticated:
        return False

    is_member = OrganizationMember.objects.filter(
        organization_id=organization_id, user=request.user, organization__is_active=True
    ).exists()

    if is_member or request.user.is_superuser:
        request.session["active_tenant_id"] = int(organization_id)
        return True
    return False
