# scripts/rdp/generators/code.py
# US-024: CLI rdp — generator kode (component, htmx, task, service, command, test, model, permission, seeder)

import os
import sys

from rdp.utils import _to_class_name, get_app_from_args, on_rm_error


def run_new_component(args):
    """Membuat Django-Cotton component HTML baru."""
    if not args:
        print("[ERROR] Penggunaan: rdp new component <nama>")
        sys.exit(1)
    name = args[0]

    components_dir = os.path.join("templates", "cotton", "rdp")
    os.makedirs(components_dir, exist_ok=True)

    file_path = os.path.join(components_dir, f"{name}.html")
    if os.path.exists(file_path):
        print(f"[ERROR] Komponen '{name}' sudah ada di '{file_path}'.")
        sys.exit(1)

    content = f"""<c-vars />

<!-- Komponen: {name} -->
<div class="rdp-{name}">
    <c-slot />
</div>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Komponen Cotton '{name}' berhasil dibuat di {file_path}")


def run_new_htmx(args):
    """Membuat Class Based View & partial template HTMX."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new htmx <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    views_dir = os.path.join(app_dir, "views")
    os.makedirs(views_dir, exist_ok=True)
    view_path = os.path.join(views_dir, f"{name}.py")

    class_name = _to_class_name(name) + "View"

    view_content = f"""from django.views.generic import TemplateView

class {class_name}(TemplateView):
    template_name = "apps/{app}/partials/{name}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tambahkan context di sini
        return context
"""
    if not os.path.exists(view_path):
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(view_content)
        print(f"  [OK] View '{class_name}' berhasil dibuat di {view_path}")
    else:
        print(f"  [WARNING] View '{name}.py' sudah ada.")

    partials_dir = os.path.join("templates", "apps", app, "partials")
    os.makedirs(partials_dir, exist_ok=True)
    partial_path = os.path.join(partials_dir, f"{name}.html")

    if not os.path.exists(partial_path):
        with open(partial_path, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Partial View: {name} -->\n<div>\n    Isi partial HTMX untuk {name}\n</div>\n")
        print(f"  [OK] Partial HTML berhasil dibuat di {partial_path}")
    else:
        print(f"  [WARNING] Partial HTML '{name}.html' sudah ada.")


def run_new_task(args):
    """Membuat background task Celery di dalam app."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new task <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    tasks_path = os.path.join(app_dir, "tasks.py")

    task_content = f"""
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def {name}():
    \"\"\"Tugas background Celery untuk {name}.\"\"\"
    try:
        logger.info("Memulai task {name}")
        # Implementasi task di sini
        pass
    except Exception as e:
        logger.error(f"Error di task {name}: {{e}}")
        raise
"""
    if not os.path.exists(tasks_path):
        with open(tasks_path, 'w', encoding='utf-8') as f:
            f.write(task_content.lstrip())
    else:
        with open(tasks_path, 'a', encoding='utf-8') as f:
            f.write(task_content)

    print(f"  [OK] Task Celery '{name}' berhasil ditambahkan di {tasks_path}")


def run_new_service(args):
    """Membuat service class di dalam app."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new service <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    services_dir = os.path.join(app_dir, "services")
    os.makedirs(services_dir, exist_ok=True)
    service_path = os.path.join(services_dir, f"{name}.py")

    if os.path.exists(service_path):
        print(f"[ERROR] Service '{name}' sudah ada.")
        sys.exit(1)

    class_name = _to_class_name(name) + "Service"

    service_content = f"""from django.db import transaction

class {class_name}:
    \"\"\"Layanan bisnis untuk {name}.\"\"\"

    @staticmethod
    @transaction.atomic
    def execute():
        \"\"\"Eksekusi logika bisnis.\"\"\"
        pass
"""
    with open(service_path, 'w', encoding='utf-8') as f:
        f.write(service_content)

    print(f"  [OK] Service '{class_name}' berhasil dibuat di {service_path}")


def run_new_command(args):
    """Membuat custom Django management command."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new command <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    commands_dir = os.path.join(app_dir, "management", "commands")
    os.makedirs(commands_dir, exist_ok=True)

    open(os.path.join(app_dir, "management", "__init__.py"), 'a').close()
    open(os.path.join(commands_dir, "__init__.py"), 'a').close()

    command_path = os.path.join(commands_dir, f"{name}.py")
    if os.path.exists(command_path):
        print(f"[ERROR] Command '{name}' sudah ada.")
        sys.exit(1)

    command_content = f"""from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deskripsi command {name}'

    def add_arguments(self, parser):
        # parser.add_argument('--force', action='store_true', help='Force execution')
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Command {name} berhasil dijalankan.'))
"""
    with open(command_path, 'w', encoding='utf-8') as f:
        f.write(command_content)

    print(f"  [OK] Custom command '{name}' berhasil dibuat di {command_path}")


def run_new_test(args):
    """Membuat file Pytest untuk app."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new test <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    tests_dir = os.path.join(app_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    open(os.path.join(tests_dir, "__init__.py"), 'a').close()

    test_path = os.path.join(tests_dir, f"test_{name}.py")
    if os.path.exists(test_path):
        print(f"[ERROR] Test 'test_{name}' sudah ada.")
        sys.exit(1)

    test_content = f"""import pytest

@pytest.mark.django_db
def test_{name}():
    # Setup

    # Execute

    # Assert
    assert True
"""
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_content)

    print(f"  [OK] File test 'test_{name}.py' berhasil dibuat di {test_path}")


def run_new_model(args):
    """Membuat model Django baru di dalam package models/."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new model <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    models_path = os.path.join(app_dir, "models", f"{name.lower()}.py")
    init_path = os.path.join(app_dir, "models", "__init__.py")
    class_name = _to_class_name(name)

    if os.path.exists(models_path):
        print(f"[ERROR] Model '{class_name}' sudah ada di {models_path}.")
        sys.exit(1)

    model_content = f"""from django.db import models

class {class_name}(models.Model):
    \"\"\"Model untuk {class_name}.\"\"\"
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "{class_name}"
        verbose_name_plural = "{class_name}s"
        db_table = "{app}_{name.lower()}"

    def __str__(self):
        return self.name
"""
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(model_content)

    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(f"from .{name.lower()} import {class_name}\n")

    print(f"  [OK] Model '{class_name}' berhasil dibuat di {models_path}")
    print("  [INFO] Jangan lupa untuk menjalankan 'rdp makemigrations' dan 'rdp migrate'.")


def run_new_permission(args):
    """Membuat file permission custom untuk app."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new permission <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    permissions_path = os.path.join(app_dir, "permissions.py")
    class_name = _to_class_name(name)

    perm_content = f"""from rest_framework import permissions

class CanView{class_name}(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('{app}.view_{name.lower()}')

class CanCreate{class_name}(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('{app}.add_{name.lower()}')

class CanUpdate{class_name}(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('{app}.change_{name.lower()}')

class CanDelete{class_name}(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('{app}.delete_{name.lower()}')
"""
    mode = 'a' if os.path.exists(permissions_path) else 'w'
    with open(permissions_path, mode, encoding='utf-8') as f:
        f.write("\n" + perm_content if mode == 'a' else perm_content)
    print(f"  [OK] Permission untuk '{class_name}' ditambahkan di {permissions_path}")


def run_new_seeder(args):
    """Membuat Django management command seeder (Faker)."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new seeder <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    commands_dir = os.path.join(app_dir, "management", "commands")
    os.makedirs(commands_dir, exist_ok=True)
    open(os.path.join(app_dir, "management", "__init__.py"), 'a').close()
    open(os.path.join(commands_dir, "__init__.py"), 'a').close()

    command_path = os.path.join(commands_dir, f"seed_{name.lower()}.py")
    class_name = _to_class_name(name)

    seeder_content = f"""from django.core.management.base import BaseCommand
from apps.{app}.models import {class_name}
from faker import Faker

class Command(BaseCommand):
    help = 'Seed data untuk {class_name}'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Jumlah data yang ingin dibuat')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker('id_ID')

        self.stdout.write(f"Membuat {{count}} {class_name}...")

        for _ in range(count):
            {class_name}.objects.create(
                name=fake.name(),
                # Tambahkan field lain dari faker di sini
            )

        self.stdout.write(self.style.SUCCESS(f"Berhasil membuat {{count}} {class_name}."))
"""
    with open(command_path, 'w', encoding='utf-8') as f:
        f.write(seeder_content)
    print(f"  [OK] Seeder command berhasil dibuat di {command_path}")


def run_remove_app(args):
    """
    TUJUAN: Hapus aplikasi Django beserta seluruh file terkait dengan konfirmasi berlapis.

    ALUR:
      1. Validasi nama app dan pastikan folder apps/<nama> ada
      2. Kumpulkan semua yang akan dihapus: folder app, templates, entri settings & urls
      3. Tampilkan daftar lengkap — tidak ada yang disembunyikan
      4. Minta user ketik ulang nama app sebagai konfirmasi (bukan Y/n)
      5. Hapus semua, laporkan hasilnya

    DIPANGGIL DARI: main() via `rdp remove app <nama-app>`
    """
    import re

    if not args:
        print("[ERROR] Nama aplikasi tidak diberikan. Penggunaan: rdp remove app <nama-app>")
        sys.exit(1)

    app_name = args[0]
    app_dir = os.path.join("apps", app_name)

    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app_name}' tidak ditemukan di '{app_dir}'.")
        sys.exit(1)

    targets = []
    targets.append(("folder", app_dir, f"apps/{app_name}/ (seluruh folder app)"))

    for tpl_path in [
        os.path.join("templates", "apps", app_name),
        os.path.join("templates", app_name),
    ]:
        if os.path.exists(tpl_path):
            targets.append(("folder", tpl_path, f"{tpl_path}/ (templates)"))

    settings_path = os.path.join("config", "settings", "base.py")
    settings_entry = f'"apps.{app_name}"'
    settings_hit = False
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            if settings_entry in f.read():
                settings_hit = True
                targets.append(("line", settings_path, f"{settings_path} — hapus baris {settings_entry}"))

    urls_path = os.path.join("config", "urls.py")
    urls_entry = f'"apps.{app_name}.urls"'
    urls_hit = False
    if os.path.exists(urls_path):
        with open(urls_path, "r", encoding="utf-8") as f:
            if urls_entry in f.read():
                urls_hit = True
                targets.append(("line", urls_path, f"{urls_path} — hapus baris include({urls_entry})"))

    _sidebar_candidates = [
        os.path.join("templates", "dashboard", "index.html"),
        os.path.join("templates", "cotton", "layout", "app.html"),
    ]
    sidebar_path = None
    sidebar_hit = False
    sidebar_pattern = f'href="/{app_name}/"'
    for _sp in _sidebar_candidates:
        if os.path.exists(_sp):
            with open(_sp, "r", encoding="utf-8") as f:
                if sidebar_pattern in f.read():
                    sidebar_path = _sp
                    sidebar_hit = True
                    targets.append(("line", sidebar_path, f"{sidebar_path} — hapus sidebar link /{app_name}/"))
                    break

    print()
    print("=" * 60)
    print(f"  [PERINGATAN] rdp remove app '{app_name}'")
    print("=" * 60)
    print("\n  Tindakan ini TIDAK BISA DIBATALKAN. Yang akan dihapus:\n")
    for _, _, label in targets:
        print(f"    ✗  {label}")
    print()

    print(f"  Untuk melanjutkan, ketik nama aplikasi: '{app_name}'")
    confirm = input("  > ").strip()
    if confirm != app_name:
        print("\n  Nama tidak cocok. Penghapusan dibatalkan.")
        sys.exit(0)

    print()

    for kind, path, label in targets:
        if kind == "folder":
            if os.path.exists(path):
                import shutil
                shutil.rmtree(path, onerror=on_rm_error)
                print(f"  [OK] Dihapus: {path}/")
        elif kind == "line":
            if path == settings_path and settings_hit:
                with open(settings_path, "r", encoding="utf-8") as f:
                    content = f.read()
                content = re.sub(
                    rf'[ \t]*"apps\.{re.escape(app_name)}"[^\n]*\n?', "", content
                )
                with open(settings_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  [OK] Entri dihapus dari {settings_path}")

            elif path == urls_path and urls_hit:
                with open(urls_path, "r", encoding="utf-8") as f:
                    content = f.read()
                content = re.sub(
                    rf'[^\n]*include\(["\']apps\.{re.escape(app_name)}\.urls["\']\)[^\n]*\n?', "", content
                )
                with open(urls_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  [OK] URL dihapus dari {urls_path}")

            elif path == sidebar_path and sidebar_hit:
                with open(sidebar_path, "r", encoding="utf-8") as f:
                    content = f.read()
                content = re.sub(
                    rf'<a[^>]*href="/{re.escape(app_name)}/"[^>]*>.*?</a>\n[ \t]*',
                    "",
                    content,
                    flags=re.DOTALL,
                )
                with open(sidebar_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  [OK] Sidebar link dihapus dari {sidebar_path}")

    print()
    print(f"  [OK] Aplikasi '{app_name}' berhasil dihapus.")
    print(f"       Jalankan 'rdp migrate' jika ada migrasi yang perlu di-rollback.")
