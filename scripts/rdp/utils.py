# scripts/rdp/utils.py
# US-024: CLI rdp — fungsi utilitas umum (prompt, git, diff, banner)

import difflib
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import urllib.request

try:
    from importlib.metadata import version as _pkg_version
    __version__ = _pkg_version("rdp-starter-kit")
except Exception:
    __version__ = "0.4.0"  # fallback saat run dari source tanpa install

TEMPLATE_REPO_URL = "https://github.com/radianapp/starterkit.git"
_PYPROJECT_RAW_URL = "https://raw.githubusercontent.com/radianapp/starterkit/main/pyproject.toml"
_CHECK_STAMP = os.path.join(os.path.expanduser("~"), ".rdp_last_update_check")
_CHECK_INTERVAL = 86400


def _fetch_latest_version() -> str | None:
    """
    TUJUAN: Ambil versi terbaru dari pyproject.toml di GitHub tanpa install apapun.

    ALUR:
      1. HTTP GET ke raw.githubusercontent.com
      2. Parse baris `version = "x.y.z"` dengan regex
      3. Return string versi atau None jika gagal (offline/timeout)

    DIPANGGIL DARI: check_for_updates(), run_upgrade_cli()
    """
    try:
        with urllib.request.urlopen(_PYPROJECT_RAW_URL, timeout=3) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        return match.group(1) if match else None
    except Exception:
        return None


def _parse_version(v: str) -> tuple:
    """'1.2.3' → (1, 2, 3) untuk perbandingan numerik."""
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0, 0, 0)


def check_for_updates() -> None:
    """
    TUJUAN: Tampilkan notifikasi jika ada versi CLI baru, maksimal sekali per hari.

    ALUR:
      1. Baca timestamp terakhir cek dari ~/.rdp_last_update_check
      2. Jika belum lewat _CHECK_INTERVAL → skip (silent)
      3. Fetch versi terbaru dari GitHub
      4. Bandingkan dengan __version__ lokal
      5. Tampilkan pesan jika ada update, update timestamp

    DIPANGGIL DARI: main() — sebelum dispatch sub-perintah
    DEPENDENSI: urllib.request, time, re
    """
    now = time.time()
    try:
        with open(_CHECK_STAMP, "r") as f:
            last_check = float(f.read().strip())
    except (OSError, ValueError):
        last_check = 0

    if now - last_check < _CHECK_INTERVAL:
        return

    try:
        with open(_CHECK_STAMP, "w") as f:
            f.write(str(now))
    except OSError:
        pass

    latest = _fetch_latest_version()
    if latest and _parse_version(latest) > _parse_version(__version__):
        print(f"\n[UPDATE] Versi baru tersedia: v{latest} (kamu v{__version__})")
        print("  Jalankan: rdp upgrade-cli")
        print()


def print_banner():
    """Tampilkan banner selamat datang."""
    print("=" * 60)
    print("      Radian Data Platform (RDP) — Project Builder CLI")
    print(f"      v{__version__}")
    print("=" * 60)


def print_help():
    """
    Tampilkan pesan bantuan penggunaan CLI.

    DIPANGGIL DARI: main() jika argumen --help atau tidak ada sub-perintah
    """
    print(f"""
rdp — CLI untuk Radian Data Platform Starter Kit v{__version__}

PENGGUNAAN:
  rdp remove app <nama_app>   Hapus aplikasi Django + templates + url + sidebar (konfirmasi berlapis)
  rdp new <nama_proyek>       Membuat proyek baru dari template RDP
  rdp new app <nama_app>      Membuat aplikasi Django baru (CLAUDE.md convention)
  rdp new api <nama_app>      Membuat skeleton REST API (DRF) di dalam aplikasi
  rdp new component <nama>    Membuat Django-Cotton component HTML
  rdp new model <nama> -a <app>   Membuat model Django
  rdp new crud <nama> -a <app>    Membuat skeleton View & HTMX partials CRUD
  rdp new page <tipe> -a <app>    Membuat halaman UI (list/create/edit/delete/detail/custom)
  rdp new service <nama> -a <app> Membuat Business Logic / Service di dalam app
  rdp new task <nama> -a <app>    Membuat background task Celery
  rdp new command <nama> -a <app> Membuat custom management command (manage.py)
  rdp new htmx <nama> -a <app>    Membuat Class Based View & partial HTML HTMX
  rdp new test <nama> -a <app>    Membuat file Pytest
  rdp new env                 Membuat file .env untuk environment
  rdp new docker              Membuat Dockerfile & docker-compose.yml
  rdp new docs                Membuat template dokumentasi standar
  rdp new permission <nama> -a <app> Membuat file permission custom
  rdp new deploy              Membuat konfigurasi deployment (nginx, systemd)
  rdp new seeder <nama> -a <app> Membuat command Django seeder (Faker)
  rdp make                    Wizard interaktif untuk generator
  rdp scaffold <nama> -a <app>Mega generator (Model, CRUD, API, Test)
  rdp assets                  Mengumpulkan dan mengkompilasi aset statis
  rdp release                 Orkestrasi sebelum rilis (lint, test, cek db)
  rdp lint                    Menjalankan ruff untuk linter & formatter
  rdp doctor                  Memeriksa kesehatan proyek & migrasi database
  rdp db <subcmd>             Utilitas database (backup, restore, reset, seed, shell)
  rdp upgrade                 Memeriksa pembaruan library (pip list --outdated)
  rdp upgrade-cli             Upgrade binary CLI rdp ke versi terbaru dari GitHub
  rdp upgrade-cli --force     Paksa upgrade meski sudah versi terbaru
  rdp monitor                 Menampilkan status monitoring sistem dasar
  rdp ai "<prompt>"           (Visi) Menggunakan AI untuk generate kode
  rdp plugin install <nama>   (Visi) Sistem manajemen plugin
  rdp build-demo              Membuat demo lengkap (app inventory beserta isinya)
  rdp update                  Memperbarui proyek saat ini dengan versi template terbaru
  rdp runserver (atau r)      Menjalankan Django dev server (uv run manage.py runserver)
  rdp migrate (atau m)        Menjalankan migrasi database (uv run manage.py migrate)
  rdp makemigrations (atau mm) Membuat file migrasi baru (uv run manage.py makemigrations)
  rdp shell (atau s)          Membuka shell interaktif Django (uv run manage.py shell)
  rdp --help                  Menampilkan bantuan ini
  rdp --version               Menampilkan versi CLI

CONTOH:
  rdp new portal-analytic
  rdp new app products
  rdp new crud produk -a inventory
  rdp new page list -a inventory --model Produk
  rdp r
  rdp update

PRASYARAT:
  - Berada di dalam direktori proyek RDP untuk perintah runserver, migrate, dll.
  - Git (https://git-scm.com) harus terinstal
  - Koneksi internet untuk mengunduh template dari GitHub (rdp new)
""")


def get_input(prompt: str, default: str | None = None) -> str:
    """
    Ambil input dari konsol dengan opsi nilai default.

    ALUR:
      1. Tampilkan prompt dengan default jika ada
      2. Loop sampai pengguna memasukkan nilai yang tidak kosong
    """
    if default:
        val = input(f"  {prompt} [{default}]: ").strip()
        return val if val else default
    else:
        while True:
            val = input(f"  {prompt}: ").strip()
            if val:
                return val


def ask_yes_no(prompt: str, default: str = "y") -> bool:
    """
    Ajukan pertanyaan ya/tidak dengan nilai default.

    ALUR:
      1. Tampilkan pilihan (Y/n) atau (y/N) sesuai default
      2. Validasi input pengguna
      3. Return True untuk ya, False untuk tidak
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    tip = "Y/n" if default == "y" else "y/N"
    while True:
        choice = input(f"  {prompt} ({tip}): ").strip().lower()
        if choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        print("  Ketik 'y' untuk ya atau 'n' untuk tidak.")


def check_git_available() -> bool:
    """
    Periksa apakah Git tersedia di sistem.

    DIPANGGIL DARI: run_new() sebelum proses cloning dimulai
    """
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def on_rm_error(func, path, exc_info):
    """Error handler untuk shutil.rmtree untuk file read-only di Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_template(target_dir: str) -> bool:
    """
    Clone template repositori dari GitHub ke direktori target.

    ALUR:
      1. Jalankan `git clone --depth=1` untuk mendapatkan versi terbaru
      2. Hapus direktori .git/ agar proyek baru tidak terhubung ke repo template
      3. Return True jika sukses, False jika gagal

    DIPANGGIL DARI: run_new()
    """
    print("\n  Mengunduh template dari GitHub...")
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", TEMPLATE_REPO_URL, target_dir],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print("\n[ERROR] Gagal mengunduh template:")
        print(f"  {e.stderr.strip()}")
        return False

    git_dir = os.path.join(target_dir, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, onerror=on_rm_error)

    return True


def show_diff(file_current, file_new):
    """Menampilkan perbedaan (diff) antara dua file."""
    try:
        with open(file_current, 'r', encoding='utf-8', errors='ignore') as f1, \
             open(file_new, 'r', encoding='utf-8', errors='ignore') as f2:
            diff = difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile='Current',
                tofile='New Template',
            )
            for line in diff:
                sys.stdout.write(line)
    except Exception as e:
        print(f"❌ Gagal membaca diff: {e}")


def prompt_overwrite(current_file, new_file, rel_path) -> bool:
    """Menampilkan prompt interaktif untuk file yang berbeda."""
    while True:
        choice = input(f"\n[UPDATE] File {rel_path} berbeda. Overwrite? [y/N/d (diff)]: ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'd':
            show_diff(current_file, new_file)
        else:
            return False


def run_django_cmd(cmd, args):
    """Menjalankan perintah Django (manage.py) via uv."""
    try:
        subprocess.run(['uv', 'run', 'python', 'manage.py', cmd] + args, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print("[ERROR] Perintah 'uv' tidak ditemukan. Pastikan uv sudah diinstal.")
        sys.exit(1)


def _to_class_name(name: str) -> str:
    """budget_item → BudgetItem"""
    return "".join(x.capitalize() for x in name.split("_"))


def get_app_from_args(args):
    """Mengekstrak nama dan parameter aplikasi dari argumen CLI."""
    if not args:
        return None, None
    name = args[0]
    app = None
    if "-a" in args:
        idx = args.index("-a")
        if idx + 1 < len(args):
            app = args[idx + 1]
    elif "--app" in args:
        idx = args.index("--app")
        if idx + 1 < len(args):
            app = args[idx + 1]
    return name, app
