"""
Decorators kustom untuk authorization di function-based views.
US: US-020 — Authorization (Permission & Group)

TUJUAN: Sediakan decorator siap pakai untuk FBV yang butuh access control
berbasis group/role — melengkapi Django bawaan @permission_required dan
@login_required.

DIPANGGIL DARI: FBV di semua app yang butuh access control
DEPENDENSI: django.contrib.auth.decorators

## CARA KERJA

Django bawaan sudah cover:
  @login_required              — cek autentikasi
  @permission_required("x.y") — cek permission tunggal

File ini menambahkan:
  @group_required("Admin")     — cek group membership
  @role_required(["A","B"])    — alias group_required, support list

CONTOH PEMAKAIAN:

  from django.contrib.auth.decorators import login_required, permission_required
  from apps.core.decorators import group_required, role_required

  # Django bawaan — cek satu permission:
  @login_required
  @permission_required("billing.add_invoice", raise_exception=True)
  def create_invoice(request):
      ...

  # Cek group:
  @login_required
  @group_required("Manager")
  def manager_dashboard(request):
      ...

  # Cek salah satu dari beberapa group:
  @login_required
  @role_required(["Manager", "Admin"])
  def sensitive_report(request):
      ...
"""

from functools import wraps

from django.core.exceptions import PermissionDenied


def group_required(*group_names: str):
    """
    TUJUAN: Batasi FBV hanya untuk user dalam group tertentu.
    US: US-020 — Authorization (Permission & Group)

    ALUR:
      1. Pastikan user authenticated (pakai @login_required sebelumnya)
      2. Superuser selalu lolos
      3. Cek user.groups terhadap group_names
      4. Tidak cocok → raise PermissionDenied (→ 403)

    DIPANGGIL DARI: FBV yang perlu dibatasi per group
    DEPENDENSI: django.core.exceptions.PermissionDenied

    PARAMETER:
      *group_names: str — nama-nama group yang diizinkan

    CONTOH:
      @login_required
      @group_required("Admin", "Manager")
      def admin_report(request):
          ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if not request.user.groups.filter(name__in=group_names).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def role_required(roles: str | list[str]):
    """
    TUJUAN: Alias group_required dengan API yang lebih eksplisit — menerima
    string tunggal atau list string.
    US: US-020 — Authorization (Permission & Group)

    ALUR:
      1. Normalisasi roles ke tuple
      2. Delegasi ke group_required

    DIPANGGIL DARI: FBV yang pakai terminologi "role" bukan "group"
    DEPENDENSI: group_required

    PARAMETER:
      roles: str | list[str] — nama role/group yang diizinkan

    CONTOH:
      @login_required
      @role_required(["Editor", "Admin"])
      def publish_post(request, pk):
          ...
    """
    if isinstance(roles, str):
        roles = [roles]
    return group_required(*roles)
