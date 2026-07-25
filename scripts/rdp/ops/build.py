# scripts/rdp/ops/build.py
# US-024: CLI rdp — operasi build (lint, doctor, db, assets, release, deploy, docs, env, docker)

import os
import shutil
import subprocess
import sys

from rdp.utils import ask_yes_no, get_input, run_django_cmd


def run_lint(args):
    """Menjalankan ruff untuk linting dan formatting."""
    print("=" * 60)
    print("  Menjalankan Code Quality Check (Ruff)...")
    print("=" * 60)
    try:
        print("\n> uv run ruff check .")
        subprocess.run(["uv", "run", "ruff", "check", "."], check=True)
        print("\n> uv run ruff format .")
        subprocess.run(["uv", "run", "ruff", "format", "."], check=True)
        print("\n  [OK] Linting dan formatting selesai!")
    except subprocess.CalledProcessError:
        print("\n  [ERROR] Linter menemukan masalah atau ruff belum terinstal.")
        sys.exit(1)
    except FileNotFoundError:
        print("\n  [ERROR] Perintah 'uv' tidak ditemukan.")
        sys.exit(1)


def run_doctor(args):
    """Memeriksa kesehatan proyek."""
    print("=" * 60)
    print("  Menjalankan Health Check...")
    print("=" * 60)

    print("\n[1/3] Memeriksa versi Python...")
    subprocess.run(["python", "--version"])

    print("\n[2/3] Memeriksa konfigurasi Django (manage.py check)...")
    try:
        subprocess.run(["uv", "run", "python", "manage.py", "check"], check=True)
    except Exception:
        print("  [ERROR] Django check gagal.")

    print("\n[3/3] Memeriksa migrasi yang terlewat...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "manage.py", "makemigrations", "--dry-run", "--check"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  [OK] Tidak ada perubahan model yang belum dibuat migrasinya.")
        else:
            print("  [WARNING] Terdapat perubahan model yang belum dimigrasi. Jalankan 'rdp makemigrations'.")
    except Exception:
        print("  [ERROR] Gagal menjalankan pengecekan migrasi.")

    print("\n  [OK] Doctor selesai berjalan.")


def run_db(args):
    """Utilitas Database."""
    if not args:
        print("Penggunaan: rdp db <backup|restore|reset|seed|shell>")
        sys.exit(1)

    subcmd = args[0]

    if subcmd == "shell":
        run_django_cmd("dbshell", args[1:])

    elif subcmd == "backup":
        output_file = args[1] if len(args) > 1 else "db_backup.json"
        print(f"Mengekspor data database ke {output_file}...")
        with open(output_file, "w", encoding='utf-8') as f:
            subprocess.run(["uv", "run", "python", "manage.py", "dumpdata"], stdout=f)
        print("  [OK] Backup selesai.")

    elif subcmd == "restore":
        if len(args) < 2:
            print("[ERROR] Mohon sebutkan file backup. Contoh: rdp db restore db_backup.json")
            sys.exit(1)
        input_file = args[1]
        print(f"Mengimpor data dari {input_file}...")
        run_django_cmd("loaddata", [input_file])
        print("  [OK] Restore selesai.")

    elif subcmd == "seed":
        fixture = args[1] if len(args) > 1 else "loaddemodata"
        if fixture == "loaddemodata":
            print("Menjalankan seeder loaddemodata...")
            run_django_cmd("loaddemodata", [])
        else:
            print(f"Menjalankan seeder loaddata {fixture}...")
            run_django_cmd("loaddata", [fixture])

    elif subcmd == "reset":
        print("[WARNING] Anda akan MENGHAPUS seluruh database sqlite3 dan menjalankan migrasi ulang.")
        confirm = ask_yes_no("Apakah Anda yakin ingin melakukan reset database?", default="n")
        if not confirm:
            print("Reset database dibatalkan.")
            return

        db_file = "db.sqlite3"
        if os.path.exists(db_file):
            os.remove(db_file)
            print("  [OK] File db.sqlite3 dihapus.")
        else:
            print("  [INFO] db.sqlite3 tidak ditemukan.")

        print("Menjalankan migrasi ulang...")
        run_django_cmd("migrate", [])

        if ask_yes_no("Apakah Anda ingin memasukkan data awal (loaddemodata) otomatis?", default="y"):
            run_django_cmd("loaddemodata", [])

        print("  [OK] Reset database selesai.")
    else:
        print(f"[ERROR] Sub-perintah db '{subcmd}' tidak dikenal.")


def run_assets(args):
    """Menjalankan kompilasi statis."""
    print("=" * 60)
    print("  Mengumpulkan & Mengkompilasi Assets...")
    print("=" * 60)
    print("\n> uv run python manage.py collectstatic --noinput")
    subprocess.run(["uv", "run", "python", "manage.py", "collectstatic", "--noinput"], check=False)
    print("\n> uv run python manage.py compress --force")
    subprocess.run(["uv", "run", "python", "manage.py", "compress", "--force"], check=False)
    print("\n  [OK] Assets siap.")


def run_release(args):
    """Orkestrasi rilis."""
    print("=" * 60)
    print("  RDP Release Preparation")
    print("=" * 60)

    print("\n[1/3] Menjalankan rdp lint...")
    try:
        run_lint([])
    except SystemExit as e:
        if e.code != 0:
            sys.exit(1)

    print("\n[2/3] Menjalankan pytest...")
    try:
        subprocess.run(["uv", "run", "pytest"], check=True)
    except subprocess.CalledProcessError:
        print("  [ERROR] Unit test gagal. Perbaiki sebelum release.")
        sys.exit(1)
    except FileNotFoundError:
        print("  [WARNING] pytest belum terinstal atau tidak ditemukan.")

    print("\n[3/3] Memeriksa migrasi & system check...")
    try:
        run_doctor([])
    except SystemExit as e:
        if e.code != 0:
            sys.exit(1)

    print("\n  [OK] Seluruh pemeriksaan rilis selesai!")


def run_new_env(args):
    """Membuat file .env untuk tiap environment."""
    envs = ['development', 'production', 'staging', 'testing']
    if not os.path.exists('.env.example'):
        print("[ERROR] File .env.example tidak ditemukan di direktori saat ini.")
        sys.exit(1)

    for env in envs:
        dest = f".env.{env}"
        if not os.path.exists(dest):
            shutil.copy2('.env.example', dest)
            print(f"  [OK] {dest} berhasil dibuat.")
        else:
            print(f"  [WARNING] {dest} sudah ada, dilewati.")


def run_new_docker(args):
    """Membuat Dockerfile & docker-compose.yml."""
    if not os.path.exists("Dockerfile"):
        dockerfile_content = """FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
"""
        with open("Dockerfile", "w", encoding='utf-8') as f:
            f.write(dockerfile_content)
        print("  [OK] Dockerfile berhasil dibuat.")
    else:
        print("  [WARNING] Dockerfile sudah ada.")

    if not os.path.exists("docker-compose.yml"):
        compose_content = """version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: rdp_db
      POSTGRES_USER: rdp_user
      POSTGRES_PASSWORD: secretpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""
        with open("docker-compose.yml", "w", encoding='utf-8') as f:
            f.write(compose_content)
        print("  [OK] docker-compose.yml berhasil dibuat.")
    else:
        print("  [WARNING] docker-compose.yml sudah ada (atau mungkin dari template).")


def run_new_docs(args):
    """Membuat template dokumentasi standar di root project."""
    print("Membuat dokumentasi proyek...")

    docs = {
        "API.md": "# API Documentation\n\nDokumentasi endpoint API ada di sini.",
        "CHANGELOG.md": "# Changelog\n\nSemua perubahan akan dicatat di file ini.",
        "CONTRIBUTING.md": "# Panduan Berkontribusi\n\nPanduan untuk developer dalam berkontribusi pada proyek ini."
    }

    for filename, content in docs.items():
        if not os.path.exists(filename):
            with open(filename, "w", encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] {filename} berhasil dibuat.")
        else:
            print(f"  [WARNING] {filename} sudah ada.")

    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding='utf-8') as f:
            f.write("# Proyek RDP\n\nProyek yang dibangun dari RDP Starter Kit.")
        print("  [OK] README.md berhasil dibuat.")

    print("  [OK] Dokumentasi proyek siap.")


def run_new_deploy(args):
    """Membuat konfigurasi deployment (nginx, systemd)."""
    print("Membuat konfigurasi deployment...")
    deploy_dir = "docker/deploy"
    os.makedirs(deploy_dir, exist_ok=True)

    nginx_conf = """server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }
}
"""
    systemd_service = """[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application

[Install]
WantedBy=multi-user.target
"""
    with open(os.path.join(deploy_dir, "nginx.conf"), "w") as f:
        f.write(nginx_conf)
    with open(os.path.join(deploy_dir, "gunicorn.service"), "w") as f:
        f.write(systemd_service)

    print(f"  [OK] File konfigurasi deployment (nginx, systemd) dibuat di {deploy_dir}/")
