#!/usr/bin/env python3
"""
CLI global untuk Radian Data Platform (RDP) Starter Kit.
US: US-024 — CLI rdp new — wizard interaktif bootstrap project

TUJUAN:
  Menyediakan perintah `rdp new <nama-proyek>` yang dapat dipanggil dari
  folder mana saja tanpa harus clone repositori ini terlebih dahulu.

CARA INSTALASI GLOBAL:
  uv tool install git+https://github.com/radianapp/starterkit.git

PENGGUNAAN:
  rdp new nama-proyek       # Bootstrap proyek baru secara interaktif
  rdp new app nama-app      # Buat aplikasi Django baru dengan struktur CLAUDE.md
  rdp new api nama-app      # Generate skeleton REST API untuk aplikasi yang ada
  rdp update                # Update proyek dari template terbaru
  rdp runserver (atau r)    # Wrapper untuk `uv run manage.py runserver`
  rdp migrate (atau m)      # Wrapper untuk `uv run manage.py migrate`
  rdp makemigrations (atau mm) # Wrapper untuk `uv run manage.py makemigrations`
  rdp shell (atau s)        # Wrapper untuk `uv run manage.py shell`
  rdp --help                # Tampilkan bantuan
  rdp --version             # Tampilkan versi

ALUR:
  1. Parse perintah (new, update, --version, --help)
  2. Jalankan wizard interaktif (nama, deskripsi, warna aksen, halaman opsional)
  3. Clone template dari GitHub ke direktori baru
  4. Bersihkan .git/, generate SECRET_KEY, setup .env
  5. Sesuaikan pyproject.toml dan urls.py dengan input pengguna
  6. Tampilkan langkah selanjutnya untuk menjalankan proyek
"""

import difflib
import filecmp
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.request

# Pastikan stdout selalu UTF-8 agar emoji dan karakter khusus tampil dengan benar di Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Versi CLI — harus sinkron dengan versi di pyproject.toml
__version__ = "0.3.1"

# URL template repositori resmi
TEMPLATE_REPO_URL = "https://github.com/radianapp/starterkit.git"

# URL raw pyproject.toml di GitHub untuk cek versi terbaru
_PYPROJECT_RAW_URL = "https://raw.githubusercontent.com/radianapp/starterkit/main/pyproject.toml"

# File penanda kapan terakhir kali cek dilakukan
_CHECK_STAMP = os.path.join(os.path.expanduser("~"), ".rdp_last_update_check")

# Interval cek update: 1 hari (dalam detik)
_CHECK_INTERVAL = 86400


def _fetch_latest_version() -> str | None:
    """
    TUJUAN: Ambil versi terbaru dari pyproject.toml di GitHub tanpa install apapun.

    ALUR:
      1. HTTP GET ke raw.githubusercontent.com
      2. Parse baris `version = "x.y.z"` dengan regex
      3. Return string versi atau None jika gagal (offline/timeout)

    DIPANGGIL DARI: check_for_updates()
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

    # Baca timestamp terakhir
    try:
        with open(_CHECK_STAMP, "r") as f:
            last_check = float(f.read().strip())
    except (OSError, ValueError):
        last_check = 0

    if now - last_check < _CHECK_INTERVAL:
        return  # Belum waktunya cek

    # Update timestamp dulu — agar gagal network pun tidak retry terus
    try:
        with open(_CHECK_STAMP, "w") as f:
            f.write(str(now))
    except OSError:
        pass

    latest = _fetch_latest_version()
    if latest and _parse_version(latest) > _parse_version(__version__):
        print(f"\n[UPDATE] Versi baru tersedia: v{latest} (kamu v{__version__})")
        print("  Upgrade: uv tool upgrade rdp-starter-kit")
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
  rdp new <nama_proyek>       Membuat proyek baru dari template RDP
  rdp new app <nama_app>      Membuat aplikasi Django baru (CLAUDE.md convention)
  rdp new api <nama_app>      Membuat skeleton REST API (DRF) di dalam aplikasi
  rdp new component <nama>    Membuat Django-Cotton component HTML
  rdp new model <nama> -a <app>   Membuat model Django
  rdp new crud <nama> -a <app>    Membuat skeleton View & HTMX partials CRUD
  rdp new service <nama> -a <app> Membuat Business Logic / Service di dalam app
  rdp new task <nama> -a <app>    Membuat background task Celery
  rdp new command <nama> -a <app> Membuat custom management command (manage.py)
  rdp new htmx <nama> -a <app>    Membuat Class Based View & partial HTML HTMX
  rdp new test <nama> -a <app>    Membuat file Pytest
  rdp new env                 Membuat file .env untuk environment
  rdp new docker              Membuat Dockerfile & docker-compose.yml
  rdp new docs                Membuat template dokumentasi standar
  rdp new page <nama> -a <app>Membuat halaman UI (template HTML utuh)
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
        subprocess.run(
            ["git", "--version"],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def on_rm_error(func, path, exc_info):
    """Error handler untuk shutil.rmtree untuk file read-only di Windows."""
    import stat
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

    # Hapus riwayat Git template agar proyek baru bersih
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


def run_update(args):
    """Jalankan proses update untuk proyek yang sudah ada."""
    if not os.path.exists("manage.py") or not os.path.exists("pyproject.toml"):
        print("❌ Error: Perintah 'rdp update' harus dijalankan di root direktori proyek RDP (yang memiliki manage.py dan pyproject.toml).")
        sys.exit(1)
        
    print(f"Mengecek pembaruan template dari: {TEMPLATE_REPO_URL}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone template to temp_dir
        if not clone_template(temp_dir):
            print("❌ Gagal mengunduh template.")
            sys.exit(1)
            
        print("✅ Template terbaru berhasil diunduh. Menganalisis perbedaan...")
        
        ignored_patterns = [
            ".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache",
            "db.sqlite3", ".env", "media", "static", "staticfiles",
            "htmlcov", ".coverage", "README.md", "CHANGELOG.md"
        ]
        
        updated_count = 0
        added_count = 0
        skipped_count = 0
        
        for root, dirs, files in os.walk(temp_dir):
            # Ignore specified directories
            dirs[:] = [d for d in dirs if d not in ignored_patterns]
            
            for file in files:
                if file in ignored_patterns:
                    continue
                    
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, temp_dir)
                dest_path = os.path.join(os.getcwd(), rel_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                if not os.path.exists(dest_path):
                    print(f"➕ Menambahkan file baru: {rel_path}")
                    shutil.copy2(src_path, dest_path)
                    added_count += 1
                else:
                    if not filecmp.cmp(src_path, dest_path, shallow=False):
                        if prompt_overwrite(dest_path, src_path, rel_path):
                            print(f"🔄 Mengupdate: {rel_path}")
                            shutil.copy2(src_path, dest_path)
                            updated_count += 1
                        else:
                            print(f"⏭️ Melewati: {rel_path}")
                            skipped_count += 1
                            
    print("\n🎉 Proses update selesai!")
    print(f"Statistik: {added_count} ditambahkan, {updated_count} diupdate, {skipped_count} dilewati.")
    print("Pastikan untuk mengecek perubahan, menjalankan `uv sync`, dan `python manage.py migrate` jika diperlukan.")


def setup_env(target_dir: str, proj_name: str, color_choice: str):
    """
    Generate file .env baru dari .env.example dengan konfigurasi proyek.

    ALUR:
      1. Baca .env.example
      2. Generate SECRET_KEY baru yang aman
      3. Isi variabel SITE_NAME, APP_BRAND_SHORT, RDP_APP_ACCENT
      4. Tulis ke file .env

    DIPANGGIL DARI: run_new()
    """
    env_example_path = os.path.join(target_dir, ".env.example")
    env_path = os.path.join(target_dir, ".env")

    if not os.path.exists(env_example_path):
        print("  [PERINGATAN] File .env.example tidak ditemukan. Lewati setup .env.")
        return

    site_name = " ".join(
        [word.capitalize() for word in proj_name.replace("-", "_").replace("_", " ").split()]
    )
    brand_short = proj_name.replace("-", "").replace("_", "")[:4].upper()
    new_secret = secrets.token_urlsafe(50)

    with open(env_example_path, encoding="utf-8") as f:
        env_lines = f.readlines()

    new_env_lines = []
    for line in env_lines:
        if line.startswith("SECRET_KEY="):
            new_env_lines.append(f"SECRET_KEY={new_secret}\n")
        elif line.startswith("SITE_NAME="):
            new_env_lines.append(f"SITE_NAME={site_name}\n")
        elif line.startswith("APP_BRAND_SHORT="):
            new_env_lines.append(f"APP_BRAND_SHORT={brand_short}\n")
        elif line.startswith("RDP_APP_ACCENT="):
            new_env_lines.append(f"RDP_APP_ACCENT={color_choice}\n")
        elif line.startswith("DEBUG="):
            new_env_lines.append("DEBUG=True\n")
        elif line.startswith("ENVIRONMENT="):
            new_env_lines.append("ENVIRONMENT=development\n")
        else:
            new_env_lines.append(line)

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_env_lines)


def setup_pyproject(target_dir: str, proj_name: str, proj_desc: str):
    """
    Ganti nama dan deskripsi di pyproject.toml dengan input pengguna.

    DIPANGGIL DARI: run_new()
    """
    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if not os.path.exists(pyproject_path):
        return

    with open(pyproject_path, encoding="utf-8") as f:
        content = f.read()

    content = content.replace('name = "rdp-starter-kit"', f'name = "{proj_name}"')
    content = content.replace(
        'description = "Production-ready Django starter template for Radian Data Platform (RDP)"',
        f'description = "{proj_desc}"',
    )

    with open(pyproject_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Update juga di uv.lock jika ada
    uv_lock_path = os.path.join(target_dir, "uv.lock")
    if os.path.exists(uv_lock_path):
        with open(uv_lock_path, encoding="utf-8") as f:
            lock_content = f.read()
        lock_content = lock_content.replace('name = "rdp-starter-kit"', f'name = "{proj_name}"')
        with open(uv_lock_path, "w", encoding="utf-8") as f:
            f.write(lock_content)


def setup_optional_pages(target_dir: str, proj_name: str, has_contact: bool, has_faq: bool):
    """
    Tambahkan URL dan template untuk halaman publik opsional (Contact Us, FAQ).

    ALUR:
      1. Modifikasi config/urls.py untuk menambahkan path baru
      2. Buat file template HTML untuk setiap halaman yang dipilih

    DIPANGGIL DARI: run_new()
    """
    site_name = " ".join(
        [word.capitalize() for word in proj_name.replace("-", "_").replace("_", " ").split()]
    )

    # Setup URL
    urls_path = os.path.join(target_dir, "config", "urls.py")
    if os.path.exists(urls_path):
        with open(urls_path, encoding="utf-8") as f:
            urls_content = f.read()

        insertion = ""
        if has_contact:
            insertion += '    path("contact/", TemplateView.as_view(template_name="public/contact.html"), name="contact"),\n'
        if has_faq:
            insertion += '    path("faq/", TemplateView.as_view(template_name="public/faq.html"), name="faq"),\n'

        if insertion:
            target_pattern = 'path("privacy/", TemplateView.as_view(template_name="public/privacy.html"), name="privacy"),'
            if target_pattern in urls_content:
                urls_content = urls_content.replace(
                    target_pattern, f"{target_pattern}\n{insertion.rstrip()}"
                )
                with open(urls_path, "w", encoding="utf-8") as f:
                    f.write(urls_content)

    # Buat file template HTML
    public_templates_dir = os.path.join(target_dir, "templates", "public")
    os.makedirs(public_templates_dir, exist_ok=True)

    if has_contact:
        contact_html = """\
<c-layout.public title="Hubungi Kami">
    <div class="container" style="max-width: 600px; padding: 40px 0;">
        <h1>Hubungi Kami</h1>
        <p>Kirim pesan kepada kami dan tim kami akan segera menghubungi Anda kembali.</p>
        <c-rdp.card>
            <form action="#" method="POST" class="rdp-form">
                <div>
                    <label for="name">Nama Lengkap</label>
                    <input type="text" id="name" name="name" placeholder="Nama Anda" required />
                </div>
                <div>
                    <label for="email">Alamat Email</label>
                    <input type="email" id="email" name="email" placeholder="nama@perusahaan.com" required />
                </div>
                <div>
                    <label for="message">Pesan Anda</label>
                    <textarea id="message" name="message" rows="5" placeholder="Tulis pesan Anda di sini..." required></textarea>
                </div>
                <c-rdp.button type="submit" variant="primary">Kirim Pesan</c-rdp.button>
            </form>
        </c-rdp.card>
    </div>
</c-layout.public>
"""
        with open(os.path.join(public_templates_dir, "contact.html"), "w", encoding="utf-8") as f:
            f.write(contact_html)

    if has_faq:
        faq_html = f"""\
<c-layout.public title="Pertanyaan Umum (FAQ)">
    <div class="container" style="max-width: 800px; padding: 40px 0; text-align: center;">
        <h1>Pertanyaan Umum (FAQ)</h1>
        <p>Temukan jawaban cepat atas pertanyaan Anda terkait platform kami.</p>

        <c-rdp.accordion>
            <c-slot name="header">Apa itu {site_name}?</c-slot>
            <p>{site_name} adalah aplikasi web modern yang dibangun di atas Radian Data Platform (RDP).</p>
        </c-rdp.accordion>

        <c-rdp.accordion>
            <c-slot name="header">Bagaimana cara memulai?</c-slot>
            <p>Daftarkan akun baru melalui halaman pendaftaran, lalu ikuti petunjuk di dashboard.</p>
        </c-rdp.accordion>

        <c-rdp.accordion>
            <c-slot name="header">Apakah data saya aman?</c-slot>
            <p>Ya. Semua komunikasi dienkripsi dengan SSL/TLS dan kata sandi dienkripsi dengan standar Django (PBKDF2).</p>
        </c-rdp.accordion>
    </div>
</c-layout.public>
"""
        with open(os.path.join(public_templates_dir, "faq.html"), "w", encoding="utf-8") as f:
            f.write(faq_html)

def cleanup_optional_features(target_dir: str, has_landing: bool, has_auth: bool, has_dashboard: bool):
    """
    Menghapus file dan routing yang tidak diinginkan pengguna saat setup "a-la-carte".
    """
    urls_path = os.path.join(target_dir, "config", "urls.py")
    settings_path = os.path.join(target_dir, "config", "settings", "base.py")
    
    if os.path.exists(urls_path):
        with open(urls_path, "r", encoding="utf-8") as f:
            urls_content = f.read()
    else:
        urls_content = ""

    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            settings_content = f.read()
    else:
        settings_content = ""

    # 1. LANDING PAGE
    if not has_landing:
        # Hapus templates/public dan templates/home.html
        public_dir = os.path.join(target_dir, "templates", "public")
        if os.path.exists(public_dir):
            shutil.rmtree(public_dir, onerror=on_rm_error)
        home_html = os.path.join(target_dir, "templates", "home.html")
        if os.path.exists(home_html):
            os.remove(home_html)
        
        # Hapus fungsi home_view beserta docstring-nya
        urls_content = re.sub(
            r'\n\ndef home_view\(request\):.*?(?=\n\nurlpatterns)',
            '',
            urls_content,
            flags=re.DOTALL,
        )
        # Hapus import redirect (tidak dipakai lagi jika tidak ada home_view)
        urls_content = re.sub(r'^from django\.shortcuts import redirect\n?', '', urls_content, flags=re.MULTILINE)
        
        # Hapus rute home (path("", ..., name="home")) — path root pakai koma, nama, argumen bervariasi
        urls_content = re.sub(r'^[ \t]*path\("",\s+\w+,\s+name="home"\),\n?', '', urls_content, flags=re.MULTILINE)
        # Hapus komentar sebelum root path
        urls_content = re.sub(r'^[ \t]*# Root.*?landing page.*?\n', '', urls_content, flags=re.MULTILINE)
        # Hapus komentar Halaman Publik
        urls_content = re.sub(r'^[ \t]*# Halaman Publik.*?\n', '', urls_content, flags=re.MULTILINE)
        # Hapus path about/terms/privacy
        urls_content = re.sub(r'^[ \t]*path\("about/".*?name="about"\),\n?', '', urls_content, flags=re.MULTILINE)
        urls_content = re.sub(r'^[ \t]*path\("terms/".*?name="terms"\),\n?', '', urls_content, flags=re.MULTILINE)
        urls_content = re.sub(r'^[ \t]*path\("privacy/".*?name="privacy"\),\n?', '', urls_content, flags=re.MULTILINE)


    # 2. AUTHENTICATION UI
    if not has_auth:
        # Hapus templates/accounts
        accounts_templates = os.path.join(target_dir, "templates", "accounts")
        if os.path.exists(accounts_templates):
            shutil.rmtree(accounts_templates, onerror=on_rm_error)
            
        # Hapus include accounts.urls
        urls_content = re.sub(r'^[ \t]*path\("accounts/", include\("apps\.accounts\.urls"\)\),\n?', '', urls_content, flags=re.MULTILINE)

    # 3. DASHBOARD UI
    if not has_dashboard:
        # Hapus apps/dashboard dan templates/dashboard
        dashboard_app = os.path.join(target_dir, "apps", "dashboard")
        dashboard_templates = os.path.join(target_dir, "templates", "dashboard")
        if os.path.exists(dashboard_app):
            shutil.rmtree(dashboard_app, onerror=on_rm_error)
        if os.path.exists(dashboard_templates):
            shutil.rmtree(dashboard_templates, onerror=on_rm_error)
            
        # Hapus dari urls.py
        urls_content = re.sub(r'^[ \t]*path\("dashboard/", include\("apps\.dashboard\.urls"\)\),\n?', '', urls_content, flags=re.MULTILINE)
        
        # Hapus dari base.py (LOCAL_APPS)
        settings_content = re.sub(r'^[ \t]*"apps\.dashboard\.apps\.DashboardConfig",\n?', '', settings_content, flags=re.MULTILINE)

    # 4. ALWAYS CLEAN HTMX EXAMPLES FOR NEW PROJECTS (unless maybe we want to keep them, but usually they are just for demo)
    # Hapus templates/htmx_examples
    htmx_templates = os.path.join(target_dir, "templates", "htmx_examples")
    if os.path.exists(htmx_templates):
        shutil.rmtree(htmx_templates, onerror=on_rm_error)
    # Hapus apps/core/views/htmx_examples.py
    htmx_views = os.path.join(target_dir, "apps", "core", "views", "htmx_examples.py")
    if os.path.exists(htmx_views):
        os.remove(htmx_views)
    # Hapus baris URL htmx
    # Karena path HTMX bisa multiline, kita hapus dari komentar Showcase sampai komentar App URLs
    urls_content = re.sub(r'^[ \t]*# Showcase 10 Pola HTMX.*?# App URLs', '    # App URLs', urls_content, flags=re.MULTILINE | re.DOTALL)
    
    # Hapus juga import htmx_views
    urls_content = re.sub(r'^[ \t]*from apps\.core\.views import htmx_examples as htmx_views\n?', '', urls_content, flags=re.MULTILINE)

    # Tulis ulang urls.py dan base.py
    if os.path.exists(urls_path):
        with open(urls_path, "w", encoding="utf-8") as f:
            f.write(urls_content)
            
    if os.path.exists(settings_path):
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write(settings_content)
def run_new(args: list[str]):
    """
    Sub-perintah `rdp new <nama-proyek>` — wizard bootstrap proyek baru.

    ALUR:
      1. Parse nama proyek dari argumen atau minta input pengguna
      2. Jalankan wizard interaktif:
         - Nama & deskripsi proyek
         - Warna aksen
         - Fitur opsional a-la-carte: Landing Page, Auth UI, Dashboard UI
      3. Clone template dari GitHub
      4. Setup .env dan pyproject.toml
      5. Hapus file/modul yang tidak dipilih (cleanup_optional_features)
      6. Jika Landing Page dipilih, tambahkan halaman Contact & FAQ
      7. Tampilkan langkah selanjutnya

    DIPANGGIL DARI: main()
    """
    print_banner()

    # Cek ketersediaan Git
    if not check_git_available():
        print("\n[ERROR] Git tidak ditemukan di sistem Anda.")
        print("  Instal Git dari https://git-scm.com lalu coba lagi.")
        sys.exit(1)

    # 1. Nama proyek
    default_name = args[0] if args else "myproject"
    print(f"\nBootstrap proyek baru dari template: {TEMPLATE_REPO_URL}\n")

    proj_name = get_input("Nama Proyek (contoh: portal-analytic)", default=default_name)
    proj_name = re.sub(r"[^a-zA-Z0-9_-]", "", proj_name)

    if not proj_name:
        print("[ERROR] Nama proyek tidak valid.")
        sys.exit(1)

    # 2. Deskripsi
    proj_desc = get_input(
        "Deskripsi Singkat Proyek",
        default="Analytic portal built on Radian Data Platform",
    )

    # 3. Warna aksen
    colors = ["teal", "coral", "purple", "amber", "gold", "navy"]
    print("\n  Pilih warna aksen aplikasi (RDP Color Coding):")
    for i, c in enumerate(colors, 1):
        print(f"    {i}. {c.capitalize()}")

    color_choice = "navy"
    while True:
        try:
            choice_idx = get_input("Pilih nomor warna aksen", default="6")
            idx = int(choice_idx) - 1
            if 0 <= idx < len(colors):
                color_choice = colors[idx]
                break
            print("  Pilihan nomor tidak valid.")
        except ValueError:
            print("  Ketik angka yang tertera.")

    # 4. Halaman dan Fitur Opsional (A-la-carte)
    print("\n  Pilih fitur yang ingin disertakan:")
    has_landing = ask_yes_no("  Sertakan halaman Landing Page Publik (home, about, privacy)?", default="y")
    has_auth = ask_yes_no("  Sertakan fitur Autentikasi UI (login, register, forgot password)?", default="y")
    has_dashboard = ask_yes_no("  Sertakan fitur Dashboard UI (dashboard, profil, aktivitas)?", default="y")

    # Tentukan direktori target
    target_dir = os.path.join(os.getcwd(), proj_name)

    if os.path.exists(target_dir):
        print(
            f"\n[ERROR] Direktori '{proj_name}' sudah ada di direktori ini."
            "\n  Silakan pilih nama lain atau hapus direktori tersebut terlebih dahulu."
        )
        sys.exit(1)

    # 5. Clone template
    print(f"\n{'=' * 60}")
    print(f"  Membuat proyek '{proj_name}'...")

    if not clone_template(target_dir):
        # Bersihkan jika clone gagal di tengah jalan
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        sys.exit(1)

    print("  Mengatur konfigurasi...")
    setup_env(target_dir, proj_name, color_choice)
    setup_pyproject(target_dir, proj_name, proj_desc)
    
    # Hapus fitur yang tidak dipilih
    cleanup_optional_features(target_dir, has_landing, has_auth, has_dashboard)
    
    # Jika Landing Page dipilih, tambahkan contact & faq karena ini bagian dari Landing Page di setup lama
    if has_landing:
        setup_optional_pages(target_dir, proj_name, True, True)

    # 7. Tampilkan instruksi selanjutnya
    print("\n" + "=" * 60)
    print(f"  [OK] Proyek '{proj_name}' berhasil dibuat!")
    print("=" * 60)
    print("\n  Langkah selanjutnya:\n")
    print(f"    cd {proj_name}")
    print("    uv sync --all-groups")
    print("    uv run python manage.py migrate")
    if has_dashboard:
        print("    uv run python manage.py loaddemodata")
    print("    uv run python manage.py createsuperuser")
    print("    uv run python manage.py runserver")
    print("\n  Buka http://localhost:8000 -- selesai!")
    print("=" * 60)


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


def run_new_app(args):
    """Membuat aplikasi Django baru dengan struktur CLAUDE.md."""
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

    # Tanya tipe aplikasi
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

    class_name = _to_class_name(app_name)           # budget → Budget, budget_item → BudgetItem
    layout = "app" if app_type == "dashboard" else "blank"
    verbose = " ".join(x.capitalize() for x in app_name.split("_"))

    print(f"\nMembuat aplikasi '{app_name}' ({app_type}) di {app_dir}/...")

    # ── models/ ──────────────────────────────────────────────────────────────
    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir)

    with open(os.path.join(models_dir, f"{app_name}.py"), "w", encoding="utf-8") as f:
        f.write(f'''\
# apps/{app_name}/models/{app_name}.py

from django.db import models
from apps.core.models import BaseModel


class {class_name}(BaseModel):
    """
    TUJUAN: Model untuk data {verbose}.

    ALUR:
      1. Simpan data {verbose} ke database
      2. [Tambahkan field sesuai kebutuhan bisnis]

    DIPANGGIL DARI: views/{app_name}.py, services/{app_name}_service.py
    DEPENDENSI: apps.core.models.BaseModel
    """

    name = models.CharField(max_length=255, verbose_name="Nama")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

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

    list_display = ["name", "is_active", "created_at"]
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

    # ── templates/ ───────────────────────────────────────────────────────────
    tpl_dir = os.path.join("templates", "apps", app_name)
    os.makedirs(tpl_dir, exist_ok=True)

    with open(os.path.join(tpl_dir, f"{app_name}_list.html"), "w", encoding="utf-8") as f:
        f.write(f'''<c-layout.{layout} title="Daftar {verbose}">
    <div class="rdp-page-header">
        <h1>Daftar {verbose}</h1>
        <a href="{{% url '{app_name}:create' %}}" role="button" class="rdp-btn rdp-btn--primary">
            + Tambah {verbose}
        </a>
    </div>

    {{% if items %}}<ul>
        {{% for item in items %}}
        <li>
            <a href="{{% url '{app_name}:detail' item.pk %}}">{{{{ item.name }}}}</a>
            &nbsp;·&nbsp;
            <a href="{{% url '{app_name}:update' item.pk %}}">Edit</a>
        </li>
        {{% endfor %}}
    </ul>
    {{% else %}}<p>Belum ada data {verbose}.</p>
    {{% endif %}}
</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_detail.html"), "w", encoding="utf-8") as f:
        f.write(f'''<c-layout.{layout} title="Detail {{{{ object.name }}}}">
    <h1>{{{{ object.name }}}}</h1>
    <p>{{{{ object.description }}}}</p>
    <a href="{{% url '{app_name}:update' object.pk %}}" role="button">Edit</a>
    <a href="{{% url '{app_name}:list' %}}">Kembali</a>
</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_form.html"), "w", encoding="utf-8") as f:
        f.write(f'''<c-layout.{layout} title="Form {verbose}">
    <h1>{{% if object %}}Edit{{% else %}}Tambah{{% endif %}} {verbose}</h1>
    <form method="POST">
        {{% csrf_token %}}
        {{{{ form.as_p }}}}
        <button type="submit">Simpan</button>
        <a href="{{% url '{app_name}:list' %}}">Batal</a>
    </form>
</c-layout.{layout}>
''')

    with open(os.path.join(tpl_dir, f"{app_name}_confirm_delete.html"), "w", encoding="utf-8") as f:
        f.write(f'''<c-layout.{layout} title="Hapus {verbose}">
    <h1>Hapus {verbose}</h1>
    <p>Yakin ingin menghapus <strong>{{{{ object.name }}}}</strong>?</p>
    <form method="POST">
        {{% csrf_token %}}
        <button type="submit" class="rdp-btn rdp-btn--danger">Hapus</button>
        <a href="{{% url '{app_name}:list' %}}">Batal</a>
    </form>
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
            # Sisipkan sebelum komentar App URLs atau sebelum urlpatterns = [
            new_path = f'    path("{app_name}/", include("apps.{app_name}.urls")),\n'
            if "# App URLs" in urls_content:
                urls_content = urls_content.replace("    # App URLs", f"    # App URLs\n{new_path}", 1)
            elif "urlpatterns = [" in urls_content:
                urls_content = urls_content.replace("urlpatterns = [", f"urlpatterns = [\n{new_path}", 1)
            with open(root_urls_path, "w", encoding="utf-8") as f:
                f.write(urls_content)
            print(f"  [OK] URL '{app_name}/' didaftarkan di config/urls.py.")

    print()
    print(f"  Langkah selanjutnya:")
    print(f"    rdp makemigrations  ← buat migrasi untuk model {class_name}")
    print(f"    rdp migrate         ← terapkan migrasi")
    if app_type == "dashboard":
        print(f"    Tambahkan <c-sidebar.link href=\"/{app_name}/\">...  ke sidebar Cotton")


def run_new_api(args):
    """Membuat skeleton REST API (DRF) di dalam aplikasi yang sudah ada."""
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
        
    # Generate api/serializers/
    serializers_dir = os.path.join(api_dir, "serializers")
    os.makedirs(serializers_dir, exist_ok=True)
    with open(os.path.join(serializers_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')
        
    # Generate api/views/
    views_dir = os.path.join(api_dir, "views")
    os.makedirs(views_dir, exist_ok=True)
    with open(os.path.join(views_dir, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')

    # Generate api/urls.py
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

def run_new_component(args):
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
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new htmx <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    # Generate View
    views_dir = os.path.join(app_dir, "views")
    os.makedirs(views_dir, exist_ok=True)
    view_path = os.path.join(views_dir, f"{name}.py")
    
    class_name = "".join(x.capitalize() or "_" for x in name.split("_")) + "View"
    
    view_content = f"""from django.views.generic import TemplateView

class {class_name}(TemplateView):
    template_name = "{app}/partials/{name}.html"

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

    # Generate Partial HTML
    partials_dir = os.path.join("templates", app, "partials")
    os.makedirs(partials_dir, exist_ok=True)
    partial_path = os.path.join(partials_dir, f"{name}.html")
    
    if not os.path.exists(partial_path):
        with open(partial_path, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Partial View: {name} -->\n<div>\n    Isi partial HTMX untuk {name}\n</div>\n")
        print(f"  [OK] Partial HTML berhasil dibuat di {partial_path}")
    else:
        print(f"  [WARNING] Partial HTML '{name}.html' sudah ada.")

def run_new_task(args):
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
        
    class_name = "".join(x.capitalize() or "_" for x in name.split("_")) + "Service"
    
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
    
    # __init__.py files
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
    class_name = "".join(x.capitalize() or "_" for x in name.split("_"))

    if os.path.exists(models_path):
        print(f"[ERROR] Model '{class_name}' sudah ada di {models_path}.")
        sys.exit(1)

    model_content = f"""from django.db import models
from apps.core.models import BaseModel

class {class_name}(BaseModel):
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

    # Otomatis export di __init__.py jika belum ada
    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(f"from .{name.lower()} import {class_name}\\n")

    print(f"  [OK] Model '{class_name}' berhasil dibuat di {models_path}")
    print("  [INFO] Jangan lupa untuk menjalankan 'rdp makemigrations' dan 'rdp migrate'.")


def run_new_crud(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new crud <nama> -a <nama-app>")
        sys.exit(1)

    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)

    class_name = "".join(x.capitalize() or "_" for x in name.split("_"))
    views_path = os.path.join(app_dir, "views", f"{name.lower()}.py")
    init_path = os.path.join(app_dir, "views", "__init__.py")

    view_content = f"""from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import {class_name}

class {class_name}ListView(ListView):
    model = {class_name}
    template_name = "{app}/{name.lower()}_list.html"
    context_object_name = "items"

class {class_name}CreateView(CreateView):
    model = {class_name}
    fields = ['name']
    template_name = "{app}/{name.lower()}_form.html"
    success_url = reverse_lazy("{app}:{name.lower()}-list")

class {class_name}UpdateView(UpdateView):
    model = {class_name}
    fields = ['name']
    template_name = "{app}/{name.lower()}_form.html"
    success_url = reverse_lazy("{app}:{name.lower()}-list")

class {class_name}DeleteView(DeleteView):
    model = {class_name}
    template_name = "{app}/{name.lower()}_confirm_delete.html"
    success_url = reverse_lazy("{app}:{name.lower()}-list")
"""
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(view_content)

    with open(init_path, 'a', encoding='utf-8') as f:
        f.write(f"from .{name.lower()} import {class_name}ListView, {class_name}CreateView, {class_name}UpdateView, {class_name}DeleteView\\n")

    # Generate Templates Dasar
    templates_dir = os.path.join("templates", app)
    os.makedirs(templates_dir, exist_ok=True)
    
    list_template = f"""<c-layout.app title="{class_name} List">
  <h1>Daftar {class_name}</h1>
  <a href="{{{{ url '{app}:{name.lower()}-create' }}}}">Tambah {class_name}</a>
  <ul>
    {{% for item in items %}}
    <li>{{{{ item.name }}}} - <a href="{{{{ url '{app}:{name.lower()}-update' item.pk }}}}">Edit</a></li>
    {{% endfor %}}
  </ul>
</c-layout.app>"""
    with open(os.path.join(templates_dir, f"{name.lower()}_list.html"), 'w', encoding='utf-8') as f:
        f.write(list_template)

    form_template = f"""<c-layout.app title="Form {class_name}">
  <h1>Form {class_name}</h1>
  <form method="POST">
    {{% csrf_token %}}
    {{{{ form.as_p }}}}
    <button type="submit">Simpan</button>
  </form>
</c-layout.app>"""
    with open(os.path.join(templates_dir, f"{name.lower()}_form.html"), 'w', encoding='utf-8') as f:
        f.write(form_template)
        
    print(f"  [OK] CRUD Skeleton untuk '{class_name}' berhasil dibuat di {views_path} dan templates/{app}/")
    print(f"  [INFO] Jangan lupa untuk mendaftarkan URL {class_name}ListView dkk di apps/{app}/urls.py.")


def run_new_env(args):
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
    # Dockerfile
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

    # docker-compose.yml
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

def run_lint(args):
    """Menjalankan ruff untuk linting dan formatting."""
    print("=" * 60)
    print("  Menjalankan Code Quality Check (Ruff)...")
    print("=" * 60)
    try:
        print("\\n> uv run ruff check .")
        subprocess.run(["uv", "run", "ruff", "check", "."], check=True)
        print("\\n> uv run ruff format .")
        subprocess.run(["uv", "run", "ruff", "format", "."], check=True)
        print("\\n  [OK] Linting dan formatting selesai!")
    except subprocess.CalledProcessError:
        print("\\n  [ERROR] Linter menemukan masalah atau ruff belum terinstal.")
        sys.exit(1)
    except FileNotFoundError:
        print("\\n  [ERROR] Perintah 'uv' tidak ditemukan.")
        sys.exit(1)


def run_doctor(args):
    """Memeriksa kesehatan proyek."""
    print("=" * 60)
    print("  Menjalankan Health Check...")
    print("=" * 60)
    
    # Cek versi python
    print("\\n[1/3] Memeriksa versi Python...")
    subprocess.run(["python", "--version"])

    # Cek django check
    print("\\n[2/3] Memeriksa konfigurasi Django (manage.py check)...")
    try:
        subprocess.run(["uv", "run", "python", "manage.py", "check"], check=True)
    except Exception:
        print("  [ERROR] Django check gagal.")
        
    # Cek migrasi yang terlewat
    print("\\n[3/3] Memeriksa migrasi yang terlewat...")
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

    print("\\n  [OK] Doctor selesai berjalan.")


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
        # Jalankan custom command loaddemodata atau loaddata
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
        
        # Tambahan: tanya apakah ingin load data demodata
        if ask_yes_no("Apakah Anda ingin memasukkan data awal (loaddemodata) otomatis?", default="y"):
            run_django_cmd("loaddemodata", [])
            
        print("  [OK] Reset database selesai.")
    else:
        print(f"[ERROR] Sub-perintah db '{subcmd}' tidak dikenal.")


def run_new_docs(args):
    """Membuat template dokumentasi standar di root project."""
    print("Membuat dokumentasi proyek...")
    
    docs = {
        "API.md": "# API Documentation\\n\\nDokumentasi endpoint API ada di sini.",
        "CHANGELOG.md": "# Changelog\\n\\nSemua perubahan akan dicatat di file ini.",
        "CONTRIBUTING.md": "# Panduan Berkontribusi\\n\\nPanduan untuk developer dalam berkontribusi pada proyek ini."
    }
    
    for filename, content in docs.items():
        if not os.path.exists(filename):
            with open(filename, "w", encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] {filename} berhasil dibuat.")
        else:
            print(f"  [WARNING] {filename} sudah ada.")
            
    # Periksa README.md
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding='utf-8') as f:
            f.write("# Proyek RDP\\n\\nProyek yang dibangun dari RDP Starter Kit.")
        print("  [OK] README.md berhasil dibuat.")
    
    print("  [OK] Dokumentasi proyek siap.")

def run_make(args):
    """Wizard interaktif untuk berbagai generator."""
    print("=" * 60)
    print("  RDP CLI - Interactive Wizard")
    print("=" * 60)
    print("Apa yang ingin dibuat?")
    print("  1. App")
    print("  2. Model")
    print("  3. CRUD")
    print("  4. API Skeleton")
    print("  5. Component Cotton")
    print("  6. Background Task (Celery)")
    print("  7. Service")
    print("  8. Test (Pytest)")
    
    choice = get_input("Pilih opsi (1-8)")
    if choice not in [str(i) for i in range(1, 9)]:
        print("[ERROR] Pilihan tidak valid.")
        return
        
    if choice == "4":
        app = get_input("Nama Aplikasi target")
        run_new_api([app])
    elif choice == "1":
        name = get_input("Nama App")
        run_new_app([name])
    elif choice == "5":
        name = get_input("Nama Component")
        run_new_component([name])
    else:
        app = get_input("Nama Aplikasi target (-a)")
        name = get_input("Nama Entitas")
        if choice == "2": run_new_model([name, "-a", app])
        elif choice == "3": run_new_crud([name, "-a", app])
        elif choice == "6": run_new_task([name, "-a", app])
        elif choice == "7": run_new_service([name, "-a", app])
        elif choice == "8": run_new_test([name, "-a", app])


def run_scaffold(args):
    """Membuat modul lengkap dari model, view, hingga API dan test."""
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp scaffold <nama> -a <nama-app>")
        sys.exit(1)
        
    print(f"\\n> Scaffold '{name}' untuk app '{app}' dimulai...")
    
    try:
        run_new_model([name, "-a", app])
    except SystemExit: pass
    
    try:
        run_new_crud([name, "-a", app])
    except SystemExit: pass
    
    try:
        run_new_api([app])
    except SystemExit: pass
    
    try:
        run_new_test([name, "-a", app])
    except SystemExit: pass
    
    print(f"\\n  [OK] Scaffold '{name}' selesai!")


def run_assets(args):
    """Menjalankan kompilasi statis."""
    print("=" * 60)
    print("  Mengumpulkan & Mengkompilasi Assets...")
    print("=" * 60)
    print("\\n> uv run python manage.py collectstatic --noinput")
    subprocess.run(["uv", "run", "python", "manage.py", "collectstatic", "--noinput"], check=False)
    
    print("\\n> uv run python manage.py compress --force")
    subprocess.run(["uv", "run", "python", "manage.py", "compress", "--force"], check=False)
    
    print("\\n  [OK] Assets siap.")


def run_release(args):
    """Orkestrasi rilis."""
    print("=" * 60)
    print("  RDP Release Preparation")
    print("=" * 60)
    
    print("\\n[1/3] Menjalankan rdp lint...")
    try:
        run_lint([])
    except SystemExit as e:
        if e.code != 0: sys.exit(1)
        
    print("\\n[2/3] Menjalankan pytest...")
    try:
        subprocess.run(["uv", "run", "pytest"], check=True)
    except subprocess.CalledProcessError:
        print("  [ERROR] Unit test gagal. Perbaiki sebelum release.")
        sys.exit(1)
    except FileNotFoundError:
        print("  [WARNING] pytest belum terinstal atau tidak ditemukan.")
        
    print("\\n[3/3] Memeriksa migrasi & system check...")
    try:
        run_doctor([])
    except SystemExit as e:
        if e.code != 0: sys.exit(1)
        
    print("\\n  [OK] Seluruh pemeriksaan rilis selesai!")

def run_new_page(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new page <nama> -a <nama-app>")
        sys.exit(1)
        
    templates_dir = os.path.join("templates", app)
    os.makedirs(templates_dir, exist_ok=True)
    page_path = os.path.join(templates_dir, f"{name.lower()}.html")
    
    if os.path.exists(page_path):
        print(f"[ERROR] Page '{name}' sudah ada di {page_path}.")
        sys.exit(1)
        
    page_content = f"""<c-layout.app title="{name.capitalize()}">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Halaman {name.capitalize()}</h1>
        <c-rdp.card>
            <p>Ini adalah halaman siap pakai untuk {name}.</p>
        </c-rdp.card>
    </div>
</c-layout.app>
"""
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"  [OK] Page '{name}' berhasil dibuat di {page_path}")


def run_new_permission(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new permission <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    permissions_path = os.path.join(app_dir, "permissions.py")
    class_name = "".join(x.capitalize() or "_" for x in name.split("_"))
    
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
        f.write("\\n" + perm_content if mode == 'a' else perm_content)
    print(f"  [OK] Permission untuk '{class_name}' ditambahkan di {permissions_path}")


def run_new_deploy(args):
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
    with open(os.path.join(deploy_dir, "nginx.conf"), "w") as f: f.write(nginx_conf)
    with open(os.path.join(deploy_dir, "gunicorn.service"), "w") as f: f.write(systemd_service)
    
    print(f"  [OK] File konfigurasi deployment (nginx, systemd) dibuat di {deploy_dir}/")


def run_new_seeder(args):
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
    class_name = "".join(x.capitalize() or "_" for x in name.split("_"))
    
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


def run_upgrade(args):
    print("=" * 60)
    print("  Memeriksa pembaruan pustaka (Dependencies)...")
    print("=" * 60)
    try:
        subprocess.run(["uv", "pip", "list", "--outdated"], check=True)
        print("\\n  [INFO] Jika ingin memperbarui, gunakan 'uv pip install --upgrade <package>'")
    except Exception:
        print("  [ERROR] Gagal menjalankan pengecekan uv pip list.")


def run_monitor(args):
    print("=" * 60)
    print("  RDP Monitor (Status Sistem)")
    print("=" * 60)
    
    import shutil
    total, used, free = shutil.disk_usage("/")
    print(f"Disk Total : {{total // (2**30)}} GiB")
    print(f"Disk Used  : {{used // (2**30)}} GiB")
    print(f"Disk Free  : {{free // (2**30)}} GiB")
    print("\\n[INFO] Untuk monitoring yang lebih lengkap, jalankan utilitas seperti 'htop' atau 'glances'.")


def run_ai(args):
    print("=" * 60)
    print("  RDP AI Assistant")
    print("=" * 60)
    if args:
        prompt = " ".join(args)
        print(f"\\nPrompt: '{prompt}'\\n")
    print("🤖 [COMING SOON] Modul RDP AI sedang dalam tahap pengembangan.")
    print("Nantinya, Anda cukup memberikan prompt dan CLI akan merancang struktur direktori, model, view, hingga HTMX secara ajaib!")


def run_plugin(args):
    print("=" * 60)
    print("  RDP Plugin System")
    print("=" * 60)
    if args and args[0] == "install":
        plugin_name = args[1] if len(args) > 1 else "<nama-plugin>"
        print(f"📦 Menginstal plugin '{plugin_name}'...")
    print("\\n[COMING SOON] Ekosistem plugin RDP sedang dirancang.")
    print("Anda akan segera bisa menambahkan fungsionalitas kompleks seperti 'blog', 'ecommerce', atau 'auditlog' hanya dengan satu perintah.")

def run_build_demo(args):
    print("=" * 60)
    print("Membangun Demo Aplikasi RDP 'inventory'...")
    print("=" * 60)
    
    commands = [
        ["new", "app", "inventory"],
        ["new", "api", "inventory"],
        ["new", "component", "status_badge"],
        ["new", "service", "stock_manager", "-a", "inventory"],
        ["new", "task", "sync_stock", "-a", "inventory"],
        ["new", "command", "import_stock", "-a", "inventory"],
        ["new", "htmx", "stock_list", "-a", "inventory"],
        ["new", "test", "stock_service", "-a", "inventory"]
    ]
    
    for cmd in commands:
        print(f"\\n> rdp {' '.join(cmd)}")
        # Untuk command new app dan new api kita perlu bypass prompt Y/n dengan Monkey Patch sementara
        if cmd[1] in ("app", "api"):
            # Mock get_input khusus untuk build-demo
            global get_input
            original_get_input = get_input
            get_input = lambda prompt, default=None: "Y"
        try:
            if cmd[1] == "app":
                run_new_app(cmd[2:])
            elif cmd[1] == "api":
                run_new_api(cmd[2:])
            elif cmd[1] == "component":
                run_new_component(cmd[2:])
            elif cmd[1] == "service":
                run_new_service(cmd[2:])
            elif cmd[1] == "task":
                run_new_task(cmd[2:])
            elif cmd[1] == "command":
                run_new_command(cmd[2:])
            elif cmd[1] == "htmx":
                run_new_htmx(cmd[2:])
            elif cmd[1] == "test":
                run_new_test(cmd[2:])
        finally:
            if cmd[1] in ("app", "api"):
                get_input = original_get_input
                
    print("\\n" + "=" * 60)
    print("  [OK] Demo 'inventory' berhasil dibangun sepenuhnya!")
    print("=" * 60)


def main():
    """
    Entry point utama untuk CLI `rdp`.

    ALUR:
      1. Periksa argumen pertama (sub-perintah)
      2. Arahkan ke fungsi yang sesuai (new, --version, --help)
      3. Tampilkan bantuan jika tidak ada argumen yang cocok

    DIPANGGIL DARI: [project.scripts] entry point di pyproject.toml
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

    if args[0] == "new":
        if len(args) > 1:
            if args[1] == "app":
                run_new_app(args[2:])
            elif args[1] == "api":
                run_new_api(args[2:])
            elif args[1] == "component":
                run_new_component(args[2:])
            elif args[1] == "htmx":
                run_new_htmx(args[2:])
            elif args[1] == "task":
                run_new_task(args[2:])
            elif args[1] == "service":
                run_new_service(args[2:])
            elif args[1] == "command":
                run_new_command(args[2:])
            elif args[1] == "test":
                run_new_test(args[2:])
            elif args[1] == "model":
                run_new_model(args[2:])
            elif args[1] == "crud":
                run_new_crud(args[2:])
            elif args[1] == "env":
                run_new_env(args[2:])
            elif args[1] == "docker":
                run_new_docker(args[2:])
            elif args[1] == "docs":
                run_new_docs(args[2:])
            elif args[1] == "page":
                run_new_page(args[2:])
            elif args[1] == "permission":
                run_new_permission(args[2:])
            elif args[1] == "deploy":
                run_new_deploy(args[2:])
            elif args[1] == "seeder":
                run_new_seeder(args[2:])
            else:
                run_new(args[1:])
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
    elif args[0] == "build-demo":
        run_build_demo(args[1:])
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
