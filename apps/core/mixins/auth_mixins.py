"""
Mixin kustom untuk authorization di CBV.
US: US-020 — Authorization (Permission & Group)

TUJUAN: Sediakan mixin siap pakai yang:
  - Redirect ke 403 (bukan login page) saat permission tidak terpenuhi
  - Support cek permission tunggal, multiple, dan group/role
  - Bisa digabung dengan LoginRequiredMixin secara alami

DIPANGGIL DARI: View CBV di semua app yang butuh access control
DEPENDENSI: django.contrib.auth.mixins.AccessMixin

## CARA KERJA

Django bawaan: PermissionRequiredMixin raise PermissionDenied (→ 403) jika
user sudah login tapi tidak punya permission. Kalau belum login, redirect ke
login page. Mixin di sini mempertahankan perilaku itu sambil menambahkan:
  1. MultiplePermissionsRequiredMixin — cek banyak permission sekaligus
  2. RoleRequiredMixin — cek berdasarkan nama group
  3. OwnerRequiredMixin — cek apakah user adalah pemilik objek

CONTOH PEMAKAIAN:

  # Cek satu permission (gunakan Django bawaan):
  from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

  class InvoiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
      permission_required = "billing.add_invoice"

  # Cek banyak permission (pakai MultiplePermissionsRequiredMixin):
  from apps.core.mixins import MultiplePermissionsRequiredMixin

  class ReportView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, TemplateView):
      permissions_required = ["analytics.view_report", "analytics.export_report"]
      require_all = True  # default True — semua harus terpenuhi

  # Cek group/role:
  from apps.core.mixins import RoleRequiredMixin

  class AdminOnlyView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
      role_required = "Admin"          # nama group di DB

  # Cek ownership:
  from apps.core.mixins import OwnerRequiredMixin

  class PostEditView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
      model = Post
      owner_field = "author"           # field FK ke user di model, default "user"
"""

from typing import ClassVar

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class MultiplePermissionsRequiredMixin(AccessMixin):
    """
    TUJUAN: Cek banyak permission sekaligus di CBV.
    US: US-020 — Authorization (Permission & Group)

    ALUR:
      1. Pastikan user sudah authenticated — kalau belum, handle_no_permission()
      2. Cek permissions_required terhadap user.has_perm() / user.has_perms()
      3. Kalau tidak terpenuhi → raise PermissionDenied (→ 403)

    DIPANGGIL DARI: CBV yang butuh lebih dari satu permission
    DEPENDENSI: django.contrib.auth.mixins.AccessMixin

    ATRIBUT:
      permissions_required: list[str] — daftar permission yang dicek
      require_all: bool — True = semua harus ada; False = cukup salah satu
    """

    permissions_required: ClassVar[list[str]] = []
    require_all: bool = True

    def get_permissions_required(self) -> list[str]:
        """Override untuk permission dinamis (misal: berdasarkan URL kwargs)."""
        return list(self.permissions_required)

    def has_permissions(self) -> bool:
        """Cek apakah user memenuhi semua/salah satu permission."""
        perms = self.get_permissions_required()
        if not perms:
            return True
        user = self.request.user
        if self.require_all:
            return user.has_perms(perms)
        return any(user.has_perm(p) for p in perms)

    def dispatch(self, request, *args, **kwargs):
        """
        TUJUAN: Gate sebelum view diproses.

        ALUR:
          1. User belum login → handle_no_permission() (redirect login)
          2. User login tapi tidak punya permission → PermissionDenied (403)
          3. Lulus → lanjut ke view

        DIPANGGIL DARI: Django CBV dispatch cycle
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.has_permissions():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RoleRequiredMixin(AccessMixin):
    """
    TUJUAN: Batasi akses berdasarkan nama Group Django.
    US: US-020 — Authorization (Permission & Group)

    ALUR:
      1. User belum login → handle_no_permission()
      2. Cek user.groups.filter(name__in=roles).exists()
      3. Tidak ada → raise PermissionDenied (403)

    DIPANGGIL DARI: CBV yang akses-nya dibatasi per role/group
    DEPENDENSI: django.contrib.auth.models.Group

    ATRIBUT:
      role_required: str | list[str] — nama group. String → dikonversi ke list.

    CONTOH:
      class ManagerView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
          role_required = ["Manager", "Admin"]
    """

    role_required: ClassVar[list[str]] = []

    def get_roles_required(self) -> list[str]:
        """Normalisasi role_required ke list."""
        roles = self.role_required
        if isinstance(roles, str):
            return [roles]
        return list(roles)

    def dispatch(self, request, *args, **kwargs):
        """
        TUJUAN: Gate akses berdasarkan group membership.

        ALUR:
          1. User belum login → handle_no_permission()
          2. Superuser selalu lolos
          3. Cek group membership → PermissionDenied jika tidak cocok

        DIPANGGIL DARI: Django CBV dispatch cycle
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Superuser bypass semua restriction
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        roles = self.get_roles_required()
        if roles and not request.user.groups.filter(name__in=roles).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(AccessMixin):
    """
    TUJUAN: Pastikan user hanya bisa akses/edit objek miliknya sendiri.
    US: US-020 — Authorization (Permission & Group)

    ALUR:
      1. User belum login → handle_no_permission()
      2. get_object() dipanggil untuk ambil instance
      3. Bandingkan getattr(obj, owner_field) dengan request.user
      4. Tidak cocok → raise PermissionDenied (403)

    DIPANGGIL DARI: CBV Detail/Update/Delete yang perlu ownership check
    DEPENDENSI: Django CBV get_object()

    ATRIBUT:
      owner_field: str — nama FK field ke user di model (default "user")

    CONTOH:
      class PostEditView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
          model = Post
          owner_field = "author"
    """

    owner_field: str = "user"

    def dispatch(self, request, *args, **kwargs):
        """
        TUJUAN: Gate akses berdasarkan ownership objek.

        ALUR:
          1. User belum login → handle_no_permission()
          2. Superuser selalu lolos
          3. get_object() → bandingkan owner dengan request.user

        DIPANGGIL DARI: Django CBV dispatch cycle
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)
        # FK bisa berupa instance User atau PK integer
        owner_pk = owner.pk if hasattr(owner, "pk") else owner
        if owner_pk != request.user.pk:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
