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

# Tambah scripts/ ke sys.path supaya package `rdp` (di scripts/rdp/) bisa diimpor
sys.path.insert(0, os.path.dirname(__file__))

# ── Utils & versi ─────────────────────────────────────────────────────────────
from rdp.utils import __version__, check_for_updates, print_help, run_django_cmd

# ── Operasi project ──────────────────────────────────────────────────────────
from rdp.ops.project import run_new, run_update

# ── Operasi build ────────────────────────────────────────────────────────────
from rdp.ops.build import (
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

# ── Operasi upgrade ───────────────────────────────────────────────────────────
from rdp.ops.upgrade import run_ai, run_monitor, run_plugin, run_upgrade, run_upgrade_cli

# ── Generator: App & API ──────────────────────────────────────────────────────
from rdp.generators.app import run_new_api, run_new_app

# ── Generator: Kode ──────────────────────────────────────────────────────────
from rdp.generators.code import (
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
from rdp.generators.crud import run_make, run_new_crud, run_new_page, run_scaffold


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
            "app":        run_new_app,
            "api":        run_new_api,
            "component":  run_new_component,
            "htmx":       run_new_htmx,
            "task":       run_new_task,
            "service":    run_new_service,
            "command":    run_new_command,
            "test":       run_new_test,
            "model":      run_new_model,
            "crud":       run_new_crud,
            "page":       run_new_page,
            "permission": run_new_permission,
            "seeder":     run_new_seeder,
            "env":        run_new_env,
            "docker":     run_new_docker,
            "docs":       run_new_docs,
            "deploy":     run_new_deploy,
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
    elif args[0] == "update":
        run_update(args[1:])
    elif args[0] in ("runserver", "r"):
        run_django_cmd("runserver", args[1:])
    elif args[0] in ("migrate", "m"):
        run_django_cmd("migrate", args[1:])
    elif args[0] in ("makemigrations", "mm"):
        run_django_cmd("makemigrations", args[1:])
    elif args[0] in ("shell", "s"):
        run_django_cmd("shell", args[1:])
    else:
        print(f"[ERROR] Sub-perintah tidak dikenal: '{args[0]}'")
        print("  Jalankan `rdp --help` untuk melihat daftar perintah yang tersedia.")
        sys.exit(1)


if __name__ == "__main__":
    main()
