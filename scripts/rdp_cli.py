#!/usr/bin/env python3
"""
CLI global untuk Radian Data Platform (RDP) Starter Kit.
US: US-024 — CLI rdp new — wizard interaktif bootstrap project

TUJUAN:
  Menyediakan perintah `rdp` yang dapat dipanggil dari folder mana saja
  tanpa harus clone repositori ini terlebih dahulu.

CARA INSTALASI GLOBAL:
  uv tool install git+https://github.com/radianapp/starterkit.git

ALUR:
  1. Parse perintah pertama (new, update, lint, db, ...)
  2. Delegasikan ke modul yang sesuai di scripts/rdp/

Modul:
  rdp/utils.py                  ← helpers, version check, banner
  rdp/ops/project.py            ← new, update
  rdp/ops/build.py              ← lint, doctor, db, assets, release
  rdp/ops/upgrade.py            ← upgrade, upgrade-cli, monitor, ai, plugin
  rdp/generators/app.py         ← new app, new api
  rdp/generators/code.py        ← new component/htmx/task/service/command/test/model/permission/seeder/remove
  rdp/generators/crud.py        ← new crud, new page, make, scaffold
"""

import os
import sys

# Prioritaskan pencarian modul local:
# 1. RDP_TEMPLATE_PATH jika di-set di environment
# 2. Current working directory jika ada folder scripts/rdp (misal di proyek lokal)
# 3. Folder lokasi rdp_cli.py ini berada
env_template_path = os.environ.get("RDP_TEMPLATE_PATH")
cwd = os.getcwd()

if env_template_path and os.path.exists(os.path.join(env_template_path, "scripts", "rdp")):
    if env_template_path not in sys.path:
        sys.path.insert(0, env_template_path)
elif os.path.exists(os.path.join(cwd, "scripts", "rdp")):
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

_cli_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_cli_dir)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)


# ── Utils & versi ─────────────────────────────────────────────────────────────
# ── Generator: App & API ──────────────────────────────────────────────────────
from scripts.rdp.generators.app import run_new_api, run_new_app

# ── Generator: Kode ──────────────────────────────────────────────────────────
from scripts.rdp.generators.code import (
    run_new_command,
    run_new_component,
    run_new_htmx,
    run_new_model,
    run_new_permission,
    run_new_seeder,
    run_new_service,
    run_new_task,
    run_new_test,
    run_remove_app,
)

# ── Generator: CRUD & Page ────────────────────────────────────────────────────
from scripts.rdp.generators.crud import run_make, run_new_crud, run_new_page, run_scaffold

# ── Operasi build ────────────────────────────────────────────────────────────
from scripts.rdp.ops.build import (
    run_assets,
    run_db,
    run_doctor,
    run_lint,
    run_new_deploy,
    run_new_docker,
    run_new_docs,
    run_new_env,
    run_release,
)

# ── Operasi project ──────────────────────────────────────────────────────────
from scripts.rdp.ops.project import run_new, run_update, run_info, run_init

# ── Operasi upgrade ───────────────────────────────────────────────────────────
from scripts.rdp.ops.upgrade import run_ai, run_monitor, run_plugin, run_upgrade, run_upgrade_cli
from scripts.rdp.utils import __version__, check_for_updates, print_help, run_django_cmd


def main():
    """
    TUJUAN: Entry point utama CLI `rdp`. Parse sub-perintah dan delegasikan.

    ALUR:
      1. Cek update versi sekali per hari (non-blocking)
      2. Parse argumen pertama (sub-perintah)
      3. Delegasikan ke fungsi yang sesuai dari submodule rdp.*

    DIPANGGIL DARI: [project.scripts] di pyproject.toml
    """
    args = sys.argv[1:]

    # Cek update sekali per hari — non-blocking, silent jika offline
    check_for_updates()

    if not args or args[0] in ("--help", "-h", "help"):
        print_help()
        return

    if args[0] in ("--version", "-v", "version"):
        print(f"rdp v{__version__}")
        return

    if args[0] == "remove":
        if len(args) > 1 and args[1] == "app":
            run_remove_app(args[2:])
        else:
            print("[ERROR] Penggunaan: rdp remove app <nama-app>")
            sys.exit(1)

    elif args[0] == "new":
        if len(args) < 2:
            run_new(args[1:])
            return

        sub = args[1]
        rest = args[2:]

        dispatch_new = {
            "app": run_new_app,
            "api": run_new_api,
            "component": run_new_component,
            "htmx": run_new_htmx,
            "task": run_new_task,
            "service": run_new_service,
            "command": run_new_command,
            "test": run_new_test,
            "model": run_new_model,
            "crud": run_new_crud,
            "page": run_new_page,
            "permission": run_new_permission,
            "seeder": run_new_seeder,
            "env": run_new_env,
            "docker": run_new_docker,
            "docs": run_new_docs,
            "deploy": run_new_deploy,
        }

        if sub in dispatch_new:
            dispatch_new[sub](rest)
        else:
            run_new(args[1:])

    elif args[0] == "lint":
        run_lint(args[1:])
    elif args[0] == "doctor":
        run_doctor(args[1:])
    elif args[0] == "db":
        run_db(args[1:])
    elif args[0] == "upgrade":
        run_upgrade(args[1:])
    elif args[0] == "upgrade-cli":
        run_upgrade_cli(args[1:])
    elif args[0] == "monitor":
        run_monitor(args[1:])
    elif args[0] == "ai":
        run_ai(args[1:])
    elif args[0] == "plugin":
        run_plugin(args[1:])
    elif args[0] == "make":
        run_make(args[1:])
    elif args[0] == "scaffold":
        run_scaffold(args[1:])
    elif args[0] == "assets":
        run_assets(args[1:])
    elif args[0] == "release":
        run_release(args[1:])
    elif args[0] == "codemap":
        import subprocess

        index_script = os.path.join(_root_dir, "scripts", "generate_docs_index.py")
        if os.path.exists(index_script):
            subprocess.run([sys.executable, index_script])
        else:
            print("[ERROR] Script generate_docs_index.py tidak ditemukan.")
    elif args[0] in ("make-crud-codemap", "crud-codemap"):
        run_django_cmd("make_crud_codemap", args[1:])
    elif args[0] in ("generate-erd", "generate_erd", "erd"):
        run_django_cmd("generate_erd", args[1:])
    elif args[0] == "update":
        run_update(args[1:])
    elif args[0] == "info":
        run_info(args[1:])
    elif args[0] == "init":
        run_init(args[1:])
    elif args[0] in ("runserver", "r"):
        run_django_cmd("runserver", args[1:])
    elif args[0] in ("migrate", "m"):
        run_django_cmd("migrate", args[1:])
    elif args[0] in ("makemigrations", "mm"):
        run_django_cmd("makemigrations", args[1:])
    elif args[0] in ("shell", "s"):
        run_django_cmd("shell", args[1:])
    elif args[0] in ("createsuperuser", "csu"):
        run_django_cmd("createsuperuser", args[1:])
    else:
        # Fallback: Jika bukan perintah RDP CLI khusus, coba jalankan sebagai perintah manage.py
        run_django_cmd(args[0], args[1:])


if __name__ == "__main__":
    main()
