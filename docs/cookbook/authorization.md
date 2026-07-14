# Authorization — Panduan Lengkap

**US-020**: Authorization (Permission & Group)  
**Ref**: `apps/core/mixins/auth_mixins.py`, `apps/core/decorators/auth_decorators.py`

---

## Konsep Dasar

Django authorization punya 3 layer:

| Layer | Apa | Contoh |
|---|---|---|
| **Permission** | Hak akses spesifik ke 1 aksi | `billing.add_invoice` |
| **Group** | Kumpulan permission bernama | `"Manager"` punya 5 permission |
| **User** | Punya group + permission langsung | user X masuk group Manager |

Semua tersimpan di DB — tidak hardcode di settings.

---

## 1. Membuat Permission

### A. Otomatis (Django default)

Setiap model Django **otomatis** mendapat 4 permission:

```
{app}.add_{model}
{app}.change_{model}
{app}.delete_{model}
{app}.view_{model}
```

Contoh: model `Invoice` di app `billing` → `billing.add_invoice`, `billing.view_invoice`, dst.

Jalankan `migrate` — permission langsung tersedia.

### B. Permission kustom (di model)

Tambahkan `Meta.permissions` di model:

```python
# apps/billing/models/invoice.py
class Invoice(models.Model):
    # ... fields ...

    class Meta:
        permissions = [
            ("can_approve_invoice", "Dapat menyetujui invoice"),
            ("can_export_invoice", "Dapat mengekspor invoice ke PDF"),
            ("can_void_invoice", "Dapat membatalkan invoice"),
        ]
```

Lalu `makemigrations` + `migrate` — permission baru muncul di admin.

**Format codename**: `{action}_{deskripsi}` — pakai snake_case, kata kerja.

### C. Permission programatik (via management command atau data migration)

```python
# apps/billing/migrations/0002_add_billing_permissions.py
from django.db import migrations


def add_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    # Permission yang tidak terkait model tertentu → pakai content type "app"
    ct, _ = ContentType.objects.get_or_create(app_label="billing", model="invoice")
    Permission.objects.get_or_create(
        codename="can_run_monthly_report",
        name="Dapat menjalankan laporan bulanan",
        content_type=ct,
    )


class Migration(migrations.Migration):
    dependencies = [("billing", "0001_initial")]
    operations = [migrations.RunPython(add_permissions, migrations.RunPython.noop)]
```

---

## 2. Membuat Group & Assign Permission

### A. Via Django Admin (paling mudah)

1. Buka `/admin/auth/group/add/`
2. Isi nama group: `"Manager"`, `"Editor"`, `"Viewer"`
3. Centang permission yang diizinkan → Save

### B. Via shell / fixture / script setup

```python
# Jalankan: uv run python manage.py shell

from django.contrib.auth.models import Group, Permission

# Buat group
manager_group, _ = Group.objects.get_or_create(name="Manager")

# Ambil permission yang ada
perms = Permission.objects.filter(codename__in=[
    "add_invoice",
    "change_invoice",
    "view_invoice",
    "can_approve_invoice",
])

# Assign permission ke group
manager_group.permissions.set(perms)
print(f"Group '{manager_group.name}' punya {manager_group.permissions.count()} permission")
```

### C. Data migration (lebih reproducible untuk tim)

```python
# apps/accounts/migrations/0003_seed_default_groups.py
from django.db import migrations


def seed_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Group Admin — akses penuh
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    admin_group.permissions.set(Permission.objects.all())

    # Group Manager — kelola invoice
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    manager_group.permissions.set(
        Permission.objects.filter(codename__in=[
            "view_invoice", "add_invoice", "change_invoice", "can_approve_invoice",
        ])
    )

    # Group Viewer — read-only
    viewer_group, _ = Group.objects.get_or_create(name="Viewer")
    viewer_group.permissions.set(
        Permission.objects.filter(codename__startswith="view_")
    )


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Admin", "Manager", "Viewer"]).delete()


class Migration(migrations.Migration):
    dependencies = [("accounts", "0002_add_extra_data_to_profile")]
    operations = [migrations.RunPython(seed_groups, remove_groups)]
```

---

## 3. Assign User ke Group

### Via Admin
Buka `/admin/accounts/user/{id}/change/` → section "Groups" → pilih group → Save.

### Via kode
```python
from django.contrib.auth.models import Group

user = request.user  # atau ambil dari DB
manager_group = Group.objects.get(name="Manager")

# Tambah ke group
user.groups.add(manager_group)

# Hapus dari group
user.groups.remove(manager_group)

# Set group (replace semua group lama)
user.groups.set([manager_group])

# Cek membership
user.groups.filter(name="Manager").exists()  # → True/False
```

---

## 4. Menggunakan di View

### Class-Based View (CBV)

#### Cek satu permission — Django bawaan

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView

from apps.billing.models import Invoice


class InvoiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Invoice
    permission_required = "billing.add_invoice"
    # raise_exception=True → 403, False (default) → redirect login
    raise_exception = True
```

#### Cek banyak permission — `MultiplePermissionsRequiredMixin`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.mixins import MultiplePermissionsRequiredMixin


class ReportExportView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, TemplateView):
    template_name = "billing/report_export.html"

    # Semua permission ini harus dipenuhi
    permissions_required = ["billing.view_invoice", "billing.can_export_invoice"]
    require_all = True  # default True

    # require_all = False → cukup salah satu


class DashboardView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    permissions_required = ["billing.view_invoice", "analytics.view_report"]
    require_all = False  # cukup salah satu → OR logic
```

#### Cek role/group — `RoleRequiredMixin`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.mixins import RoleRequiredMixin


class ManagerDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "dashboard/manager.html"
    role_required = "Manager"           # string → satu group


class AdminOrManagerView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "dashboard/restricted.html"
    role_required = ["Admin", "Manager"]  # list → salah satu cukup
```

#### Cek ownership objek — `OwnerRequiredMixin`

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from apps.core.mixins import OwnerRequiredMixin
from apps.blog.models import Post


class PostEditView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    owner_field = "author"   # nama FK field ke user di model Post
    # default owner_field = "user"
```

#### Permission dinamis (berdasarkan URL kwargs)

```python
from apps.core.mixins import MultiplePermissionsRequiredMixin


class ProjectView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, DetailView):
    model = Project

    def get_permissions_required(self):
        # Permission berbeda tergantung URL
        if self.kwargs.get("mode") == "edit":
            return ["projects.change_project"]
        return ["projects.view_project"]
```

---

### Function-Based View (FBV)

#### Django bawaan — `@login_required` + `@permission_required`

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


@login_required
@permission_required("billing.add_invoice", raise_exception=True)
def create_invoice(request):
    return render(request, "billing/create.html")
```

#### Cek group/role — `@group_required`, `@role_required`

```python
from django.contrib.auth.decorators import login_required

from apps.core.decorators import group_required, role_required


# Cek satu group
@login_required
@group_required("Manager")
def manager_report(request):
    return render(request, "reports/manager.html")


# Cek banyak group (salah satu cukup)
@login_required
@group_required("Admin", "Manager")
def sensitive_action(request):
    return render(request, "admin/action.html")


# Alias — lebih eksplisit
@login_required
@role_required(["Editor", "Admin"])
def publish_article(request, pk):
    ...
```

---

## 5. Cek Permission di Template

```django
{# Tampilkan tombol hanya jika user punya permission #}
{% if perms.billing.add_invoice %}
    <c-rdp.button variant="primary" href="{% url 'billing:invoice_create' %}">
        Buat Invoice
    </c-rdp.button>
{% endif %}

{# Cek membership group — perlu context processor atau tag kustom #}
{# Cara termudah: lewat view, set variabel is_manager #}
{% if is_manager %}
    <a href="{% url 'dashboard:manager' %}">Manager Dashboard</a>
{% endif %}
```

Di view:
```python
def dashboard(request):
    return render(request, "dashboard/index.html", {
        "is_manager": request.user.groups.filter(name="Manager").exists(),
    })
```

---

## 6. Cek Permission di Kode Python

```python
# Cek permission tunggal
request.user.has_perm("billing.add_invoice")           # → True/False

# Cek banyak permission (semua harus ada)
request.user.has_perms(["billing.add_invoice", "billing.can_approve_invoice"])

# Cek group
request.user.groups.filter(name="Manager").exists()

# Cek superuser (bypass semua restriction)
request.user.is_superuser

# Cek staff (akses admin panel)
request.user.is_staff
```

---

## 7. Urutan Mixin yang Benar

MRO (Method Resolution Order) Django CBV penting. Urutan yang benar:

```python
# ✅ BENAR: LoginRequired dulu, baru permission check
class MyView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    ...

class MyView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    ...

# ❌ SALAH: permission check sebelum login check
class MyView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    ...
```

`LoginRequiredMixin` harus paling kiri — ini memastikan user anonymous di-redirect ke login sebelum dicek permission-nya.

---

## 8. Troubleshooting

**Permission tidak terdeteksi padahal sudah di-assign?**
Django cache permission di request pertama. Setelah assign permission, reload user dari DB:
```python
user = User.objects.get(pk=user.pk)
# atau
from django.contrib.auth import get_user_model
user.refresh_from_db()
```

Di test, selalu ambil ulang user setelah `user_permissions.add()`:
```python
user.user_permissions.add(perm)
user = User.objects.get(pk=user.pk)  # clear cache
```

**Group baru tidak muncul di admin?**
Pastikan sudah `migrate`. Permission dan group dibuat saat migrasi.

**Superuser selalu lolos?**
Ya — `is_superuser=True` bypass semua `has_perm()` check. `RoleRequiredMixin` dan `@group_required` juga explicit bypass superuser. Ini by design.
