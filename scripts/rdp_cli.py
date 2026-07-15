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
  rdp update                # Update proyek dari template terbaru
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

# Versi CLI — harus sinkron dengan versi di pyproject.toml
__version__ = "0.3.0"

# URL template repositori resmi
TEMPLATE_REPO_URL = "https://github.com/radianapp/starterkit.git"


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
  rdp new <nama_proyek>  Membuat proyek baru dari template RDP
  rdp update             Memperbarui proyek saat ini dengan versi template terbaru
  rdp --help             Menampilkan bantuan ini
  rdp --version          Menampilkan versi CLI

CONTOH:
  rdp new portal-analytic
  rdp update

PRASYARAT:
  - Git (https://git-scm.com) harus terinstal
  - Koneksi internet untuk mengunduh template dari GitHub
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


def run_new(args: list[str]):
    """
    Sub-perintah `rdp new <nama-proyek>` — wizard bootstrap proyek baru.

    ALUR:
      1. Parse nama proyek dari argumen atau minta input pengguna
      2. Jalankan wizard interaktif (deskripsi, warna, halaman opsional)
      3. Clone template dari GitHub
      4. Setup .env, pyproject.toml, dan halaman opsional
      5. Tampilkan langkah selanjutnya

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

    # 4. Halaman opsional
    has_contact = ask_yes_no("\n  Tambahkan halaman publik 'Contact Us'?", default="y")
    has_faq = ask_yes_no("  Tambahkan halaman publik 'FAQ'?", default="y")

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

    # 6. Setup konfigurasi
    print("  Mengatur konfigurasi...")
    setup_env(target_dir, proj_name, color_choice)
    setup_pyproject(target_dir, proj_name, proj_desc)
    setup_optional_pages(target_dir, proj_name, has_contact, has_faq)

    # 7. Tampilkan instruksi selanjutnya
    print("\n" + "=" * 60)
    print(f"  [SUCCESS] Proyek '{proj_name}' berhasil dibuat!")
    print("=" * 60)
    print("\n  Langkah selanjutnya:\n")
    print(f"    cd {proj_name}")
    print("    uv sync --all-groups")
    print("    uv run python manage.py migrate")
    print("    uv run python manage.py loaddemodata")
    print("    uv run python manage.py createsuperuser")
    print("    uv run python manage.py runserver")
    print("\n  Buka http://localhost:8000 — selesai! 🚀")
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

    if not args or args[0] in ("--help", "-h", "help"):
        print_help()
        return

    if args[0] in ("--version", "-v", "version"):
        print(f"rdp v{__version__}")
        return

    if args[0] == "new":
        run_new(args[1:])
    elif args[0] == "update":
        run_update(args[1:])
    else:
        print(f"[ERROR] Sub-perintah tidak dikenal: '{args[0]}'")
        print("  Jalankan `rdp --help` untuk melihat daftar perintah yang tersedia.")
        sys.exit(1)


if __name__ == "__main__":
    main()
