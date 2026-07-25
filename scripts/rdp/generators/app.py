# scripts/rdp/generators/app.py
# US-024: CLI rdp — generator app Django baru dan skeleton API

import os
import re
import sys

from ..utils import _to_class_name, get_input, on_rm_error


def run_new_app(args):
    """
    TUJUAN: Membuat aplikasi Django baru dengan struktur CLAUDE.md (package per fungsi).

    ALUR:
      1. Validasi nama app
      2. Tanya tipe (dashboard / blank)
      3. Generate seluruh struktur: models/, views/, services/, forms/, admin/, tests/, apps.py, urls.py
      4. Buat templates di templates/apps/{app_name}/
      5. Daftarkan ke LOCAL_APPS, config/urls.py, dan sidebar

    DIPANGGIL DARI: main() via `rdp new app <nama>`
    """
    if not args:
        print("[ERROR] Nama aplikasi tidak diberikan. Penggunaan: rdp new app <nama-app>")
        sys.exit(1)

    app_name = args[0]
    if not re.match(r'^[a-zA-Z0-9_]+$', app_name):
        print("[ERROR] Nama aplikasi hanya boleh mengandung huruf, angka, dan underscore.")
        sys.exit(1)

    apps_dir = "apps"
    if not os.path.exists(apps_dir):
        print("[ERROR] Direktori 'apps' tidak ditemukan. Jalankan perintah ini di root proyek RDP.")
        sys.exit(1)

    app_dir = os.path.join(apps_dir, app_name)
    if os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app_name}' sudah ada di '{app_dir}'.")
        sys.exit(1)

    print("\n  Tipe aplikasi:")
    print("    1. Dashboard — dilindungi login, muncul di sidebar app")
    print("    2. Blank     — standalone, tidak ada di sidebar")

    app_type = "dashboard"
    while True:
        choice = get_input("Pilih tipe (1/2)", default="1")
        if choice == "1":
            app_type = "dashboard"
            break
        elif choice == "2":
            app_type = "blank"
            break
        print("  Ketik 1 atau 2.")

    class_name = _to_class_name(app_name)
    layout = "app" if app_type == "dashboard" else "blank"
    verbose = " ".join(x.capitalize() for x in app_name.split("_"))

    print(f"\nMembuat aplikasi '{app_name}' ({app_type}) di {app_dir}/...")

    # ── models/ ──────────────────────────────────────────────────────────────
    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir)

    with open(os.path.join(models_dir, f"{app_name}.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/models/{app_name}.py

from django.conf import settings
from django.db import models


class {class_name}(models.Model):
    """
    TUJUAN: Model untuk data {verbose}.

    ALUR:
      1. Simpan data {verbose} ke database
      2. [Tambahkan field sesuai kebutuhan bisnis]

    DIPANGGIL DARI: views/{app_name}.py, services/{app_name}_service.py
    DEPENDENSI: django.db.models.Model
    """

    name = models.CharField(max_length=255, verbose_name="Nama")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="{app_name}_{class_name.lower()}_created",
        verbose_name="Dibuat oleh",
    )

    class Meta:
        verbose_name = "{verbose}"
        verbose_name_plural = "{verbose}"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
''')

    with open(os.path.join(models_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
from .{app_name} import {class_name}

__all__ = ["{class_name}"]
''')

    # ── views/ ───────────────────────────────────────────────────────────────
    views_dir = os.path.join(app_dir, "views")
    os.makedirs(views_dir)

    with open(os.path.join(views_dir, f"{app_name}.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/views/{app_name}.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..models import {class_name}
from ..forms import {class_name}Form


class {class_name}ListView(LoginRequiredMixin, ListView):
    """
    TUJUAN: Tampilkan daftar semua {verbose}.

    DIPANGGIL DARI: urls.py → path("", ..., name="list")
    DEPENDENSI: {class_name} model, templates/apps/{app_name}/{app_name}_list.html
    """

    model = {class_name}
    template_name = "apps/{app_name}/{app_name}_list.html"
    context_object_name = "items"


class {class_name}DetailView(LoginRequiredMixin, DetailView):
    """
    TUJUAN: Tampilkan detail satu {verbose}.

    DIPANGGIL DARI: urls.py → path("<int:pk>/", ..., name="detail")
    """

    model = {class_name}
    template_name = "apps/{app_name}/{app_name}_detail.html"


class {class_name}CreateView(LoginRequiredMixin, CreateView):
    """
    TUJUAN: Buat {verbose} baru.

    DIPANGGIL DARI: urls.py → path("baru/", ..., name="create")
    """

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app_name}/{app_name}_form.html"
    success_url = reverse_lazy("{app_name}:list")


class {class_name}UpdateView(LoginRequiredMixin, UpdateView):
    """
    TUJUAN: Edit {verbose} yang sudah ada.

    DIPANGGIL DARI: urls.py → path("<int:pk>/edit/", ..., name="update")
    """

    model = {class_name}
    form_class = {class_name}Form
    template_name = "apps/{app_name}/{app_name}_form.html"
    success_url = reverse_lazy("{app_name}:list")


class {class_name}DeleteView(LoginRequiredMixin, DeleteView):
    """
    TUJUAN: Hapus {verbose}.

    DIPANGGIL DARI: urls.py → path("<int:pk>/hapus/", ..., name="delete")
    """

    model = {class_name}
    template_name = "apps/{app_name}/{app_name}_confirm_delete.html"
    success_url = reverse_lazy("{app_name}:list")
''')

    with open(os.path.join(views_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
from .{app_name} import (
    {class_name}ListView,
    {class_name}DetailView,
    {class_name}CreateView,
    {class_name}UpdateView,
    {class_name}DeleteView,
)

__all__ = [
    "{class_name}ListView",
    "{class_name}DetailView",
    "{class_name}CreateView",
    "{class_name}UpdateView",
    "{class_name}DeleteView",
]
''')

    # ── services/ ────────────────────────────────────────────────────────────
    services_dir = os.path.join(app_dir, "services")
    os.makedirs(services_dir)

    with open(os.path.join(services_dir, f"{app_name}_service.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/services/{app_name}_service.py

from django.db import transaction

from ..models import {class_name}


class {class_name}Service:
    """
    TUJUAN: Layanan bisnis untuk entitas {verbose}.

    ALUR:
      1. Terima data dari views atau Celery tasks
      2. Proses bisnis (validasi, kalkulasi, transformasi, dll.)
      3. Simpan ke database via model

    DIPANGGIL DARI: views/{app_name}.py, tasks/ (jika ada)
    DEPENDENSI: {class_name} model
    """

    @staticmethod
    @transaction.atomic
    def create(data: dict) -> "{class_name}":
        """
        TUJUAN: Buat {verbose} baru dengan validasi bisnis.

        ALUR:
          1. Validasi data input
          2. Buat instance {class_name}
          3. Return instance yang tersimpan
        """
        return {class_name}.objects.create(**data)

    @staticmethod
    @transaction.atomic
    def update(instance: "{class_name}", data: dict) -> "{class_name}":
        """
        TUJUAN: Update data {verbose} yang sudah ada.
        """
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance: "{class_name}") -> None:
        """
        TUJUAN: Hapus {verbose}.
        """
        instance.delete()
''')

    with open(os.path.join(services_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
from .{app_name}_service import {class_name}Service

__all__ = ["{class_name}Service"]
''')

    # ── forms/ ───────────────────────────────────────────────────────────────
    forms_dir = os.path.join(app_dir, "forms")
    os.makedirs(forms_dir)

    with open(os.path.join(forms_dir, f"{app_name}_forms.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/forms/{app_name}_forms.py

from django import forms

from ..models import {class_name}


class {class_name}Form(forms.ModelForm):
    """
    TUJUAN: Form untuk create dan update {verbose}.

    DIPANGGIL DARI: views/{app_name}.py ({class_name}CreateView, {class_name}UpdateView)
    DEPENDENSI: {class_name} model
    """

    class Meta:
        model = {class_name}
        fields = ["name", "description", "is_active"]
        widgets = {{
            "description": forms.Textarea(attrs={{"rows": 4}}),
        }}
''')

    with open(os.path.join(forms_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
from .{app_name}_forms import {class_name}Form

__all__ = ["{class_name}Form"]
''')

    # ── admin/ ───────────────────────────────────────────────────────────────
    admin_dir = os.path.join(app_dir, "admin")
    os.makedirs(admin_dir)

    with open(os.path.join(admin_dir, f"{app_name}_admin.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/admin/{app_name}_admin.py

from django.contrib import admin

from ..models import {class_name}


@admin.register({class_name})
class {class_name}Admin(admin.ModelAdmin):
    """
    TUJUAN: Konfigurasi tampilan {verbose} di Django Admin.

    DIPANGGIL DARI: Django admin auto-discovery
    DEPENDENSI: {class_name} model
    """

    list_display = ["name", "is_active", "created_at", "created_by"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]
''')

    with open(os.path.join(admin_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
from .{app_name}_admin import {class_name}Admin

__all__ = ["{class_name}Admin"]
''')

    # ── tests/ ───────────────────────────────────────────────────────────────
    tests_dir = os.path.join(app_dir, "tests")
    os.makedirs(tests_dir)

    with open(os.path.join(tests_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    with open(os.path.join(tests_dir, f"test_{app_name}.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/tests/test_{app_name}.py

import pytest
from django.urls import reverse

from apps.{app_name}.models import {class_name}


@pytest.mark.django_db
class Test{class_name}Model:
    """Test untuk model {verbose}."""

    def test_str(self):
        obj = {class_name}(name="Test {verbose}")
        assert str(obj) == "Test {verbose}"

    def test_default_active(self):
        obj = {class_name}.objects.create(name="Test Aktif")
        assert obj.is_active is True


@pytest.mark.django_db
class Test{class_name}Views:
    """Test untuk views {verbose}."""

    def test_list_requires_login(self, client):
        url = reverse("{app_name}:list")
        response = client.get(url)
        # Redirect ke halaman login jika belum login
        assert response.status_code == 302
''')

    # ── apps.py ──────────────────────────────────────────────────────────────
    with open(os.path.join(app_dir, "apps.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/apps.py

from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{app_name}"
    verbose_name = "{verbose}"
''')

    # ── urls.py ──────────────────────────────────────────────────────────────
    with open(os.path.join(app_dir, "urls.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/urls.py

from django.urls import path

from .views import (
    {class_name}ListView,
    {class_name}DetailView,
    {class_name}CreateView,
    {class_name}UpdateView,
    {class_name}DeleteView,
)

app_name = "{app_name}"

urlpatterns = [
    path("", {class_name}ListView.as_view(), name="list"),
    path("<int:pk>/", {class_name}DetailView.as_view(), name="detail"),
    path("baru/", {class_name}CreateView.as_view(), name="create"),
    path("<int:pk>/edit/", {class_name}UpdateView.as_view(), name="update"),
    path("<int:pk>/hapus/", {class_name}DeleteView.as_view(), name="delete"),
]
''')

    # ── migrations/ ──────────────────────────────────────────────────────────
    migrations_dir = os.path.join(app_dir, "migrations")
    os.makedirs(migrations_dir)
    with open(os.path.join(migrations_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    # ── templates/ ───────────────────────────────────────────────────────────
    tpl_dir = os.path.join("templates", "apps", app_name)
    os.makedirs(tpl_dir, exist_ok=True)

    with open(os.path.join(tpl_dir, f"{app_name}_list.html"), "w", encoding="utf-8") as f:
        f.write(f'''\
{{# {app_name}/templates/apps/{app_name}/{app_name}_list.html #}}
<c-layout.{layout} title="Daftar {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Daftar {verbose}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="primary" href="{{% url '{app_name}:create' %}}">+ Tambah {verbose}</c-rdp.button>
        </div>
    </div>

    <c-rdp.card>
        {{% if items %}}
        <table class="rdp-table">
            <thead>
                <tr>
                    <th>Nama</th>
                    <th>Status</th>
                    <th>Dibuat</th>
                    <th style="width:120px">Aksi</th>
                </tr>
            </thead>
            <tbody>
                {{% for item in items %}}
                <tr>
                    <td><a href="{{% url '{app_name}:detail' item.pk %}}">{{{{ item.name }}}}</a></td>
                    <td>
                        {{% if item.is_active %}}
                            <span class="rdp-badge rdp-badge--success">Aktif</span>
                        {{% else %}}
                            <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
                        {{% endif %}}
                    </td>
                    <td>{{{{ item.created_at|date:"d M Y" }}}}</td>
                    <td class="rdp-table__actions">
                        <a href="{{% url '{app_name}:update' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--secondary">Edit</a>
                        <a href="{{% url '{app_name}:delete' item.pk %}}" class="rdp-btn rdp-btn--sm rdp-btn--danger">Hapus</a>
                    </td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>
        {{% else %}}
        <div class="rdp-empty-state">
            <p class="rdp-empty-state__text">Belum ada data {verbose}.</p>
            <c-rdp.button variant="primary" href="{{% url '{app_name}:create' %}}">+ Tambah {verbose}</c-rdp.button>
        </div>
        {{% endif %}}
    </c-rdp.card>

</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_detail.html"), "w", encoding="utf-8") as f:
        f.write(f'''\
{{# {app_name}/templates/apps/{app_name}/{app_name}_detail.html #}}
<c-layout.{layout} title="{{{{ object.name }}}}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">{{{{ object.name }}}}</h2>
        <div class="rdp-page-header__actions">
            <c-rdp.button variant="secondary" href="{{% url '{app_name}:update' object.pk %}}">Edit</c-rdp.button>
            <c-rdp.button variant="danger" href="{{% url '{app_name}:delete' object.pk %}}">Hapus</c-rdp.button>
        </div>
    </div>

    <c-rdp.card>
        <dl class="rdp-dl">
            <dt>Nama</dt>
            <dd>{{{{ object.name }}}}</dd>

            <dt>Deskripsi</dt>
            <dd>{{{{ object.description|default:"-" }}}}</dd>

            <dt>Status</dt>
            <dd>
                {{% if object.is_active %}}
                    <span class="rdp-badge rdp-badge--success">Aktif</span>
                {{% else %}}
                    <span class="rdp-badge rdp-badge--neutral">Nonaktif</span>
                {{% endif %}}
            </dd>

            <dt>Dibuat pada</dt>
            <dd>{{{{ object.created_at|date:"d M Y H:i" }}}}</dd>

            {{% if object.created_by %}}
            <dt>Dibuat oleh</dt>
            <dd>{{{{ object.created_by }}}}</dd>
            {{% endif %}}
        </dl>
    </c-rdp.card>

    <div style="margin-top:16px">
        <a href="{{% url '{app_name}:list' %}}" class="rdp-btn rdp-btn--ghost">← Kembali ke Daftar</a>
    </div>

</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_form.html"), "w", encoding="utf-8") as f:
        f.write(f'''\
{{# {app_name}/templates/apps/{app_name}/{app_name}_form.html #}}
<c-layout.{layout} title="{{% if object %}}Edit{{% else %}}Tambah{{% endif %}} {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">{{% if object %}}Edit{{% else %}}Tambah{{% endif %}} {verbose}</h2>
    </div>

    <c-rdp.card>
        <form method="POST" class="rdp-form">
            {{% csrf_token %}}
            {{{{ form.as_p }}}}
            <div class="rdp-form__actions">
                <c-rdp.button type="submit" variant="primary">Simpan</c-rdp.button>
                <c-rdp.button variant="ghost" href="{{% url '{app_name}:list' %}}">Batal</c-rdp.button>
            </div>
        </form>
    </c-rdp.card>

</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_confirm_delete.html"), "w", encoding="utf-8") as f:
        f.write(f'''\
{{# {app_name}/templates/apps/{app_name}/{app_name}_confirm_delete.html #}}
<c-layout.{layout} title="Hapus {verbose}">

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Hapus {verbose}</h2>
    </div>

    <c-rdp.card>
        <p>Yakin ingin menghapus <strong>{{{{ object.name }}}}</strong>? Tindakan ini tidak bisa dibatalkan.</p>
        <form method="POST" style="margin-top:16px; display:flex; gap:8px">
            {{% csrf_token %}}
            <c-rdp.button type="submit" variant="danger">Ya, Hapus</c-rdp.button>
            <c-rdp.button variant="ghost" href="{{% url '{app_name}:list' %}}">Batal</c-rdp.button>
        </form>
    </c-rdp.card>

</c-layout.{layout}>
''')

    print(f"  [OK] Struktur aplikasi '{app_name}' ({app_type}) berhasil dibuat.")

    # ── Daftarkan ke LOCAL_APPS ───────────────────────────────────────────────
    base_settings_path = os.path.join("config", "settings", "base.py")
    if os.path.exists(base_settings_path):
        ans = get_input(f"Daftarkan 'apps.{app_name}' ke LOCAL_APPS di config/settings/base.py? (Y/n)", default="Y")
        if ans.lower() in ("y", "yes"):
            with open(base_settings_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "LOCAL_APPS = [" in content:
                content = content.replace("LOCAL_APPS = [", f'LOCAL_APPS = [\n    "apps.{app_name}",')
                with open(base_settings_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print("  [OK] Aplikasi didaftarkan di LOCAL_APPS.")
            else:
                print("  [WARNING] Blok LOCAL_APPS tidak ditemukan. Daftarkan manual.")
    else:
        print(f"\n  [INFO] Tambahkan 'apps.{app_name}' ke LOCAL_APPS di settings.")

    # ── Daftarkan URL di config/urls.py ───────────────────────────────────────
    root_urls_path = os.path.join("config", "urls.py")
    if os.path.exists(root_urls_path):
        ans = get_input(f"Tambahkan path('{app_name}/', ...) ke config/urls.py? (Y/n)", default="Y")
        if ans.lower() in ("y", "yes"):
            with open(root_urls_path, "r", encoding="utf-8") as f:
                urls_content = f.read()
            new_path = f'    path("{app_name}/", include("apps.{app_name}.urls")),\n'
            if "# App URLs" in urls_content:
                urls_content = urls_content.replace("    # App URLs", f"    # App URLs\n{new_path}", 1)
            elif "urlpatterns = [" in urls_content:
                urls_content = urls_content.replace("urlpatterns = [", f"urlpatterns = [\n{new_path}", 1)
            with open(root_urls_path, "w", encoding="utf-8") as f:
                f.write(urls_content)
            print(f"  [OK] URL '{app_name}/' didaftarkan di config/urls.py.")

    # ── Tambahkan link ke sidebar ──────────────────────────────────────────────
    marker = "{# rdp:sidebar-links — marker untuk rdp new app, jangan hapus #}"
    _sidebar_candidates = [
        os.path.join("templates", "dashboard", "index.html"),
        os.path.join("templates", "cotton", "layout", "app.html"),
    ]
    _sidebar_files_with_marker = [
        p for p in _sidebar_candidates
        if os.path.exists(p) and marker in open(p, encoding="utf-8").read()
    ]

    if app_type == "dashboard" and _sidebar_files_with_marker:
        ans = get_input(f"Tambahkan link '{verbose}' ke sidebar? (Y/n)", default="Y")
        if ans.lower() in ("y", "yes"):
            for sidebar_path in _sidebar_files_with_marker:
                with open(sidebar_path, "r", encoding="utf-8") as f:
                    sidebar_content = f.read()
                link_class = "rdp-sidebar__link" if "rdp-sidebar__link" in sidebar_content else "sidebar-link"
                icon_class = "rdp-sidebar__link-icon" if "rdp-sidebar__link-icon" in sidebar_content else "icon-circle"
                text_class = "rdp-sidebar__link-text" if "rdp-sidebar__link-text" in sidebar_content else ""
                icon_html = f'<span class="{icon_class}">🔗</span>'
                text_html = (
                    f'<span class="{text_class}">{verbose}</span>' if text_class
                    else f'<span>{verbose}</span>'
                )
                indent = "                "
                sidebar_link = (
                    f'<a href="/{app_name}/" class="{link_class}">\n'
                    f'{indent}    {icon_html}\n'
                    f'{indent}    {text_html}\n'
                    f'{indent}</a>\n'
                    f'{indent}{marker}'
                )
                sidebar_content = sidebar_content.replace(marker, sidebar_link, 1)
                with open(sidebar_path, "w", encoding="utf-8") as f:
                    f.write(sidebar_content)
                print(f"  [OK] Link '{verbose}' ditambahkan ke sidebar ({sidebar_path}).")
    elif app_type == "dashboard":
        print(f"  [WARNING] Marker sidebar tidak ditemukan. Tambahkan manual: " + marker)

    print()
    print(f"  Langkah selanjutnya:")
    print(f"    rdp makemigrations  ← buat migrasi untuk model {class_name}")
    print(f"    rdp migrate         ← terapkan migrasi")


def run_new_api(args):
    """
    TUJUAN: Membuat skeleton REST API (DRF) di dalam aplikasi yang sudah ada.

    DIPANGGIL DARI: main() via `rdp new api <nama-app>`
    """
    if not args:
        print("[ERROR] Nama aplikasi tidak diberikan. Penggunaan: rdp new api <nama-app>")
        sys.exit(1)

    app_name = args[0]
    apps_dir = "apps"
    app_dir = os.path.join(apps_dir, app_name)

    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app_name}' tidak ditemukan di '{app_dir}'.")
        print("  Buat aplikasi terlebih dahulu dengan: rdp new app " + app_name)
        sys.exit(1)

    api_dir = os.path.join(app_dir, "api")
    if os.path.exists(api_dir):
        ans = get_input(f"Folder 'api/' sudah ada di dalam '{app_name}'. Timpa isi folder? (y/N)", default="N")
        if ans.lower() not in ("y", "yes"):
            print("Operasi dibatalkan.")
            sys.exit(0)
    else:
        os.makedirs(api_dir)

    with open(os.path.join(api_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')

    serializers_dir = os.path.join(api_dir, "serializers")
    os.makedirs(serializers_dir, exist_ok=True)
    with open(os.path.join(serializers_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')

    views_dir = os.path.join(api_dir, "views")
    os.makedirs(views_dir, exist_ok=True)
    with open(os.path.join(views_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')

    urls_content = f"""from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "{app_name}_api"
router = DefaultRouter()
# Daftarkan ViewSet Anda di sini
# router.register(r'items', views.ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
"""
    with open(os.path.join(api_dir, 'urls.py'), 'w', encoding='utf-8') as f:
        f.write(urls_content)

    print(f"  [OK] Skeleton REST API untuk '{app_name}' berhasil dibuat di {api_dir}/")
    print(f"  [INFO] Jangan lupa untuk mendaftarkan 'apps.{app_name}.api.urls' di config/api_urls.py (jika menggunakan router global) atau config/urls.py.")
