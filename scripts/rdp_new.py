#!/usr/bin/env python3
"""
CLI wizard to bootstrap a new Radian Data Platform (RDP) project from the starter kit.
US: US-024 — CLI rdp new — wizard interaktif bootstrap project
"""

import os
import re
import secrets
import shutil
import sys


def get_input(prompt, default=None):
    """Get input from console with a default option."""
    if default:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    else:
        while True:
            val = input(f"{prompt}: ").strip()
            if val:
                return val


def ask_yes_no(prompt, default="y"):
    """Ask a yes/no question."""
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default == "y":
        tip = "Y/n"
    else:
        tip = "y/N"

    while True:
        choice = input(f"{prompt} ({tip}): ").strip().lower()
        if choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        print("Ketik 'y' untuk ya atau 'n' untuk tidak.")


def main():  # noqa: C901
    print("=" * 60)
    print("      Radian Data Platform (RDP) Project Builder Wizard")
    print("=" * 60)

    # 1. Project name
    default_name = "myproject"
    if len(sys.argv) > 1:
        default_name = sys.argv[1]

    proj_name = get_input("Nama Proyek (contoh: portal-analytic)", default=default_name)
    # Clean project name to alphanumeric / hyphen
    proj_name = re.sub(r"[^a-zA-Z0-9_-]", "", proj_name)

    # 2. Description
    proj_desc = get_input(
        "Deskripsi Singkat Proyek", default="Analytic portal built on Radian Data Platform"
    )

    # 3. Accent color
    colors = ["teal", "coral", "purple", "amber", "gold", "navy"]
    print("\nPilih warna aksen aplikasi (RDP Color Coding):")
    for i, c in enumerate(colors, 1):
        print(f"  {i}. {c.capitalize()}")

    color_choice = "navy"
    while True:
        try:
            choice_idx = get_input("Pilih nomor warna aksen", default="6")
            idx = int(choice_idx) - 1
            if 0 <= idx < len(colors):
                color_choice = colors[idx]
                break
            print("Pilihan nomor tidak valid.")
        except ValueError:
            print("Ketik angka yang tertera.")

    # 4. Optional pages
    has_contact = ask_yes_no("\nApakah Anda membutuhkan halaman Publik 'Contact Us'?", default="y")
    has_faq = ask_yes_no("Apakah Anda membutuhkan halaman Publik 'FAQ'?", default="y")

    # Target path
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(os.getcwd(), proj_name)

    if os.path.exists(target_dir):
        print(
            f"\n[ERROR] Direktori '{proj_name}' sudah ada. Silakan pilih nama lain atau hapus direktori tersebut."
        )
        sys.exit(1)

    print(f"\nMembuat proyek '{proj_name}' di {target_dir}...")

    # Exclusions for copying
    exclude_dirs = {
        ".git",
        ".venv",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
        "rdp_starter_kit.egg-info",
        "new_project",
        proj_name,
    }
    exclude_files = {".coverage", "db.sqlite3"}

    # Copy files
    os.makedirs(target_dir)
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(target_dir, item)

        if os.path.isdir(src_item):
            if item in exclude_dirs:
                continue
            shutil.copytree(
                src_item,
                dst_item,
                ignore=shutil.ignore_patterns(
                    "*.pyc", "__pycache__", ".venv", ".git", ".pytest_cache", ".ruff_cache"
                ),
            )
        else:
            if item in exclude_files:
                continue
            shutil.copy2(src_item, dst_item)

    # 5. Generate secure random SECRET_KEY
    new_secret = secrets.token_urlsafe(50)

    # 6. Setup .env
    env_example_path = os.path.join(target_dir, ".env.example")
    env_path = os.path.join(target_dir, ".env")

    # Generate SITE_NAME from project name
    site_name = " ".join(
        [word.capitalize() for word in proj_name.replace("-", "_").replace("_", " ").split()]
    )
    brand_short = proj_name.replace("-", "").replace("_", "")[:4].upper()

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

    # 7. Rename references to rdp-starter-kit or rdp_starter_kit in files
    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, encoding="utf-8") as f:
            content = f.read()
        content = content.replace('name = "rdp-starter-kit"', f'name = "{proj_name}"')
        content = content.replace(
            'description = "Production-ready Django starter template for Radian Data Platform (RDP)"',
            f'description = "{proj_desc}"',
        )
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(content)

    uv_lock_path = os.path.join(target_dir, "uv.lock")
    if os.path.exists(uv_lock_path):
        with open(uv_lock_path, encoding="utf-8") as f:
            content = f.read()
        content = content.replace('name = "rdp-starter-kit"', f'name = "{proj_name}"')
        with open(uv_lock_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 8. Handle optional pages: Contact Us & FAQ
    urls_path = os.path.join(target_dir, "config", "urls.py")
    if os.path.exists(urls_path):
        with open(urls_path, encoding="utf-8") as f:
            urls_content = f.read()

        # We will insert new path rules right below about/terms/privacy
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

    # Write HTML files if selected
    public_templates_dir = os.path.join(target_dir, "templates", "public")
    os.makedirs(public_templates_dir, exist_ok=True)

    if has_contact:
        contact_html = """<c-layout.public title="Hubungi Kami">
    <div class="container" style="max-width: 600px; padding: 40px 0;">
        <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">Hubungi Kami</h1>
        <p style="color: var(--pico-muted-color); margin-bottom: 30px;">Kirim pesan kepada kami dan tim kami akan segera menghubungi Anda kembali.</p>

        <c-rdp.card>
            <form action="#" method="POST" class="rdp-form">
                <div style="margin-bottom: 16px;">
                    <label for="name">Nama Lengkap</label>
                    <input type="text" id="name" name="name" placeholder="Nama Anda" required />
                </div>
                <div style="margin-bottom: 16px;">
                    <label for="email">Alamat Email</label>
                    <input type="email" id="email" name="email" placeholder="nama@perusahaan.com" required />
                </div>
                <div style="margin-bottom: 24px;">
                    <label for="message">Pesan Anda</label>
                    <textarea id="message" name="message" rows="5" placeholder="Tulis pesan Anda di sini..." required></textarea>
                </div>
                <c-rdp.button type="submit" variant="primary" style="width: 100%;">Kirim Pesan</c-rdp.button>
            </form>
        </c-rdp.card>
    </div>
</c-layout.public>
"""
        with open(os.path.join(public_templates_dir, "contact.html"), "w", encoding="utf-8") as f:
            f.write(contact_html)

    if has_faq:
        faq_html = f"""<c-layout.public title="Pertanyaan Umum (FAQ)">
    <div class="container" style="max-width: 800px; padding: 40px 0;">
        <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 8px; text-align: center;">Pertanyaan Umum (FAQ)</h1>
        <p style="color: var(--pico-muted-color); margin-bottom: 40px; text-align: center;">Temukan jawaban cepat atas pertanyaan Anda terkait platform kami.</p>

        <c-rdp.accordion>
            <c-slot name="header">Apa itu {site_name}?</c-slot>
            <p>{site_name} adalah aplikasi web modern yang dibangun di atas Radian Data Platform (RDP) menggunakan framework Django dan PicoCSS.</p>
        </c-rdp.accordion>

        <c-rdp.accordion style="margin-top: 12px;">
            <c-slot name="header">Bagaimana cara memulai?</c-slot>
            <p>Anda dapat mendaftarkan akun baru melalui halaman pendaftaran, lalu mengikuti petunjuk pengaturan di dashboard untuk mulai menggunakan platform.</p>
        </c-rdp.accordion>

        <c-rdp.accordion style="margin-top: 12px;">
            <c-slot name="header">Apakah data saya aman?</c-slot>
            <p>Ya, keamanan data Anda adalah prioritas kami. Semua komunikasi dienkripsi menggunakan SSL/TLS dan kata sandi dienkripsi dengan standar Django (PBKDF2).</p>
        </c-rdp.accordion>
    </div>
</c-layout.public>
"""
        with open(os.path.join(public_templates_dir, "faq.html"), "w", encoding="utf-8") as f:
            f.write(faq_html)

    print("\n" + "=" * 60)
    print("[SUCCESS] Proyek RDP baru Anda telah berhasil di-bootstrap!")
    print("=" * 60)
    print("\nLangkah selanjutnya untuk mulai menjalankan:")
    print("  1. Masuk ke direktori proyek:")
    print(f"     cd {proj_name}")
    print("  2. Jalankan uv sync:")
    print("     uv sync")
    print("  3. Jalankan migrasi basis data:")
    print("     uv run python manage.py migrate")
    print("  4. Buat akun superuser:")
    print("     uv run python manage.py createsuperuser")
    print("  5. Jalankan server pembangunan:")
    print("     uv run python manage.py runserver")
    print("=" * 60)


if __name__ == "__main__":
    main()
