# scripts/rdp/ops/project.py
# US-024: CLI rdp — operasi project-level (new, update, setup)

import filecmp
import os
import re
import secrets
import shutil
import sys
import tempfile

from ..utils import (
    ask_yes_no,
    check_git_available,
    clone_template,
    get_input,
    on_rm_error,
    print_banner,
    prompt_overwrite,
)


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

    uv_lock_path = os.path.join(target_dir, "uv.lock")
    if os.path.exists(uv_lock_path):
        with open(uv_lock_path, encoding="utf-8") as f:
            lock_content = f.read()
        lock_content = lock_content.replace('name = "rdp-starter-kit"', f'name = "{proj_name}"')
        with open(uv_lock_path, "w", encoding="utf-8") as f:
            f.write(lock_content)


def reset_project_scaffolding(target_dir: str, proj_name: str, proj_desc: str):
    """
    Mereset folder/file bawaan starterkit agar siap digunakan untuk project baru.
    (Misalnya menghapus docs bawaan, tests bawaan, dan reset CHANGELOG/README).
    """
    # 1. Reset docs/
    docs_dir = os.path.join(target_dir, "docs")
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir, onerror=on_rm_error)
    os.makedirs(docs_dir, exist_ok=True)

    # 2. Reset tests/
    tests_dir = os.path.join(target_dir, "tests")
    if os.path.exists(tests_dir):
        shutil.rmtree(tests_dir, onerror=on_rm_error)
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    # 3. Reset CHANGELOG.md
    changelog_path = os.path.join(target_dir, "CHANGELOG.md")
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(
            f"# Changelog\\n\\nAll notable changes to {proj_name} will be documented in this file.\\n\\n## [Unreleased]\\n"
        )

    # 4. Reset README.md
    readme_path = os.path.join(target_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {proj_name}\\n\\n{proj_desc}\\n")

    # 5. Hapus blok [project.scripts] dari pyproject.toml
    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"\[project\.scripts\]\\n.*?(\\n\[)", r"\\1", content, flags=re.DOTALL)
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 6. Hapus folder/file yang tidak perlu di-copy (misalnya bin, instalation scripts, dll)
    unnecessary = [
        ".agents",
        ".claude",
        "logs",
        "media",
        "scratch_test_dir",
        "build",
        "dist",
        "bin",
        "scripts",
        "install.ps1",
        "install.sh",
        "backup.bundle",
        "tags-backup.txt",
        "layout_dump.html",
        "fix_bools.py",
        "scratch_gens.py",
    ]
    for item in unnecessary:
        p = os.path.join(target_dir, item)
        if os.path.isdir(p):
            shutil.rmtree(p, onerror=on_rm_error)
        elif os.path.isfile(p):
            try:
                os.remove(p)
            except OSError:
                pass


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


def cleanup_optional_features(
    target_dir: str,
    has_landing: bool,
    has_auth: bool,
    has_dashboard: bool,
    has_demo_pages: bool = True,
):
    """
    Menghapus file dan routing yang tidak diinginkan pengguna saat setup "a-la-carte".

    DIPANGGIL DARI: run_new()
    """
    urls_path = os.path.join(target_dir, "config", "urls.py")
    settings_path = os.path.join(target_dir, "config", "settings", "base.py")

    if os.path.exists(urls_path):
        with open(urls_path, encoding="utf-8") as f:
            urls_content = f.read()
    else:
        urls_content = ""

    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as f:
            settings_content = f.read()
    else:
        settings_content = ""

    if not has_landing:
        public_dir = os.path.join(target_dir, "templates", "public")
        if os.path.exists(public_dir):
            shutil.rmtree(public_dir, onerror=on_rm_error)
        home_html = os.path.join(target_dir, "templates", "home.html")
        if os.path.exists(home_html):
            os.remove(home_html)

    if not has_auth:
        accounts_templates = os.path.join(target_dir, "templates", "accounts")
        if os.path.exists(accounts_templates):
            shutil.rmtree(accounts_templates, onerror=on_rm_error)
        urls_content = re.sub(
            r'^[ \t]*path\("accounts/", include\("apps\.accounts\.urls"\)\),\n?',
            "",
            urls_content,
            flags=re.MULTILINE,
        )

    if not has_dashboard:
        dashboard_app = os.path.join(target_dir, "apps", "dashboard")
        dashboard_templates = os.path.join(target_dir, "templates", "dashboard")
        if os.path.exists(dashboard_app):
            shutil.rmtree(dashboard_app, onerror=on_rm_error)
        if os.path.exists(dashboard_templates):
            shutil.rmtree(dashboard_templates, onerror=on_rm_error)
        urls_content = re.sub(
            r'^[ \t]*path\("dashboard/", include\("apps\.dashboard\.urls"\)\),\n?',
            "",
            urls_content,
            flags=re.MULTILINE,
        )
        settings_content = re.sub(
            r'^[ \t]*"apps\.dashboard\.apps\.DashboardConfig",\n?',
            "",
            settings_content,
            flags=re.MULTILINE,
        )

    if not has_demo_pages:
        for demo_dir in ["htmx_examples", "starter", "docs"]:
            p = os.path.join(target_dir, "templates", demo_dir)
            if os.path.exists(p):
                shutil.rmtree(p, onerror=on_rm_error)
        dev_comp = os.path.join(target_dir, "templates", "dev_components.html")
        if os.path.exists(dev_comp):
            os.remove(dev_comp)

        # Hapus demo apps (inventory, test_app) jika demo pages tidak diaktifkan
        for demo_app in ["inventory", "test_app"]:
            app_p = os.path.join(target_dir, "apps", demo_app)
            if os.path.exists(app_p):
                shutil.rmtree(app_p, onerror=on_rm_error)

        for demo_view_file in ["htmx_examples.py", "starter.py"]:
            v_p = os.path.join(target_dir, "apps", "core", "views", demo_view_file)
            if os.path.exists(v_p):
                os.remove(v_p)

        # Bersihkan referensi apps.inventory dan apps.test_app dari settings dan urls
        settings_content = re.sub(
            r'^[ \t]*"apps\.inventory.*?",?\n?', "", settings_content, flags=re.MULTILINE
        )
        settings_content = re.sub(
            r'^[ \t]*"apps\.test_app.*?",?\n?', "", settings_content, flags=re.MULTILINE
        )
        urls_content = re.sub(
            r'\nif is_app_installed\("apps\.inventory"\):\n\s+urlpatterns\.append\(path\("produk/", include\("apps\.inventory\.urls"\)\)\)',
            "",
            urls_content,
        )

        urls_content = re.sub(
            r"\n[ \t]*# Docs & Examples.*?(?=\n[ \t]*# Halaman Publik|\n[ \t]*# App URLs)",
            "",
            urls_content,
            flags=re.MULTILINE | re.DOTALL,
        )
        urls_content = re.sub(
            r"\n[ \t]*# HTMX Examples.*?(?=\n[ \t]*# App URLs)",
            "",
            urls_content,
            flags=re.MULTILINE | re.DOTALL,
        )
        urls_content = re.sub(
            r"^from apps\.core\.views import StarterDocsView.*?\n",
            "",
            urls_content,
            flags=re.MULTILINE,
        )
        urls_content = re.sub(
            r"^from apps\.core\.views import htmx_examples as htmx_views\n?",
            "",
            urls_content,
            flags=re.MULTILINE,
        )

    else:
        htmx_templates = os.path.join(target_dir, "templates", "htmx_examples")
        if os.path.exists(htmx_templates):
            shutil.rmtree(htmx_templates, onerror=on_rm_error)
        htmx_views_file = os.path.join(target_dir, "apps", "core", "views", "htmx_examples.py")
        if os.path.exists(htmx_views_file):
            os.remove(htmx_views_file)
        urls_content = re.sub(
            r"^[ \t]*# Showcase 10 Pola HTMX.*?# App URLs",
            "    # App URLs",
            urls_content,
            flags=re.MULTILINE | re.DOTALL,
        )
        urls_content = re.sub(
            r"^[ \t]*from apps\.core\.views import htmx_examples as htmx_views\n?",
            "",
            urls_content,
            flags=re.MULTILINE,
        )

    if not has_demo_pages and has_dashboard:
        dash_partials = os.path.join(target_dir, "templates", "dashboard", "partials")
        if os.path.exists(dash_partials):
            shutil.rmtree(dash_partials, onerror=on_rm_error)

        dash_index = os.path.join(target_dir, "templates", "dashboard", "index.html")
        if os.path.exists(dash_index):
            with open(dash_index, "w", encoding="utf-8") as f:
                f.write("""\
{# US-010: Dashboard page — halaman utama setelah login #}
{% load static %}
{% load cotton %}

<c-layout.app title="Dashboard" navbar_brand="Dashboard">

    <c-slot name="head">
        <link rel="stylesheet" href="{% static 'css/dashboard.css' %}">
    </c-slot>

    <c-slot name="sidebar">
        <a href="/" class="rdp-sidebar__brand">
            <span class="rdp-sidebar__brand-icon">⬡</span>
            <span class="rdp-sidebar__brand-text">{{ APP_BRAND_SHORT }}</span>
        </a>

        <nav class="rdp-sidebar__nav" aria-label="Main navigation">
            <div class="rdp-sidebar__section">
                <div class="rdp-sidebar__section-title">Menu Utama</div>
                <a href="{% url 'dashboard:index' %}" class="rdp-sidebar__link active" aria-current="page">
                    <span class="rdp-sidebar__link-icon">📊</span>
                    <span class="rdp-sidebar__link-text">Dashboard</span>
                </a>
                {# rdp:sidebar-links — marker untuk rdp new app, jangan hapus #}
            </div>

            <div class="rdp-sidebar__section">
                <div class="rdp-sidebar__section-title">Pengaturan</div>
                {% if user.is_authenticated %}
                    <a href="{% url 'accounts:profile' %}" class="rdp-sidebar__link">
                        <span class="rdp-sidebar__link-icon">👤</span>
                        <span class="rdp-sidebar__link-text">Profil</span>
                    </a>
                    <a href="{% url 'admin:index' %}" class="rdp-sidebar__link">
                        <span class="rdp-sidebar__link-icon">⚙️</span>
                        <span class="rdp-sidebar__link-text">Admin</span>
                    </a>
                {% endif %}
            </div>
        </nav>

        <div class="rdp-sidebar__footer" x-data="{ open: false }" @click.away="open = false">
            <button type="button" class="rdp-sidebar__link rdp-sidebar__user-btn"
                    @click="open = !open" :aria-expanded="open" aria-haspopup="true">
                <div class="rdp-avatar rdp-avatar--sm rdp-sidebar__footer-avatar">
                    <span class="rdp-avatar__initials">{{ user.get_full_name|default:user.email|slice:":2"|upper }}</span>
                </div>
                <span class="rdp-sidebar__link-text">{{ user.get_full_name|default:user.email }}</span>
                <span class="rdp-sidebar__user-chevron" :class="{ 'is-open': open }">▲</span>
            </button>

            <div x-show="open" class="rdp-user-menu" role="menu">
                <a href="{% url 'accounts:profile' %}" class="rdp-user-menu__item" role="menuitem">
                    <span class="rdp-user-menu__icon">👤</span> Profil
                </a>
                <div class="rdp-user-menu__divider" role="separator"></div>
                <form method="post" action="{% url 'accounts:logout' %}" class="rdp-user-menu__form">
                    {% csrf_token %}
                    <button type="submit" class="rdp-user-menu__item rdp-user-menu__item--danger" role="menuitem">
                        <span class="rdp-user-menu__icon">🚪</span> Keluar
                    </button>
                </form>
            </div>
        </div>
    </c-slot>

    <div class="rdp-page-header">
        <h2 class="rdp-page-header__title">Selamat Datang, {{ user.get_full_name|default:user.email }}</h2>
    </div>

    <p style="color: var(--rdp-text-muted); margin-top: 8px;">
        Aplikasi siap digunakan. Mulai tambah fitur dengan <code>rdp new app &lt;nama&gt;</code>.
    </p>

</c-layout.app>
""")

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
      2. Jalankan wizard interaktif (nama, deskripsi, warna, fitur opsional)
      3. Clone template dari GitHub
      4. Setup .env dan pyproject.toml
      5. Hapus file/modul yang tidak dipilih (cleanup_optional_features)
      6. Tampilkan langkah selanjutnya

    DIPANGGIL DARI: main()
    """
    print_banner()

    if not check_git_available():
        print("\n[ERROR] Git tidak ditemukan di sistem Anda.")
        print("  Instal Git dari https://git-scm.com lalu coba lagi.")
        sys.exit(1)

    use_local = "--local" in args or "-l" in args
    clean_args = [a for a in args if a not in ("--local", "-l")]

    default_name = clean_args[0] if clean_args else "myproject"
    print("\nBootstrap proyek baru dari template: https://github.com/radianapp/starterkit.git\n")

    proj_name = get_input("Nama Proyek (contoh: portal-analytic)", default=default_name)
    proj_name = re.sub(r"[^a-zA-Z0-9_-]", "", proj_name)

    if not proj_name:
        print("[ERROR] Nama proyek tidak valid.")
        sys.exit(1)

    proj_desc = get_input(
        "Deskripsi Singkat Proyek",
        default="Analytic portal built on Radian Data Platform",
    )

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

    print("\n  Pilih fitur yang ingin disertakan:")
    has_landing = ask_yes_no(
        "  Sertakan halaman Landing Page Publik (home, about, privacy)?", default="y"
    )
    has_auth = True  # Autentikasi sekarang menjadi requirement wajib
    has_dashboard = ask_yes_no(
        "  Sertakan fitur Dashboard UI (dashboard, profil, aktivitas)?", default="y"
    )
    has_demo_pages = ask_yes_no(
        "  Sertakan halaman demo/dokumentasi (docs/, examples/, HTMX showcase)?", default="n"
    )

    target_dir = os.path.join(os.getcwd(), proj_name)

    if os.path.exists(target_dir):
        print(
            f"\n[ERROR] Direktori '{proj_name}' sudah ada di direktori ini."
            "\n  Silakan pilih nama lain atau hapus direktori tersebut terlebih dahulu."
        )
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  Membuat proyek '{proj_name}'...")

    # Lokasi root starterkit lokal untuk testing pengembangan tanpa push ke GitHub
    local_starterkit_root = (
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        if use_local
        else None
    )

    if not clone_template(target_dir, source_path=local_starterkit_root):
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        sys.exit(1)

    print("  Mengatur konfigurasi...")
    setup_env(target_dir, proj_name, color_choice)
    setup_pyproject(target_dir, proj_name, proj_desc)
    reset_project_scaffolding(target_dir, proj_name, proj_desc)
    cleanup_optional_features(target_dir, has_landing, has_auth, has_dashboard, has_demo_pages)

    if has_landing:
        setup_optional_pages(target_dir, proj_name, True, True)

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


def run_update(args):
    """Jalankan proses update untuk proyek yang sudah ada."""

    if not os.path.exists("manage.py") or not os.path.exists("pyproject.toml"):
        print(
            "[ERROR] Perintah 'rdp update' harus dijalankan di root direktori proyek RDP (yang memiliki manage.py dan pyproject.toml)."
        )
        sys.exit(1)

    print("Mengecek pembaruan template dari: https://github.com/radianapp/starterkit.git")

    with tempfile.TemporaryDirectory() as temp_dir:
        if not clone_template(temp_dir):
            print("[ERROR] Gagal mengunduh template.")
            sys.exit(1)

        print("[OK] Template terbaru berhasil diunduh. Menganalisis perbedaan...")

        ignored_patterns = [
            ".git",
            ".venv",
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
            "db.sqlite3",
            ".env",
            "media",
            "static",
            "staticfiles",
            "htmlcov",
            ".coverage",
            "README.md",
            "CHANGELOG.md",
        ]

        updated_count = 0
        added_count = 0
        skipped_count = 0

        for root, dirs, files in os.walk(temp_dir):
            dirs[:] = [d for d in dirs if d not in ignored_patterns]

            for file in files:
                if file in ignored_patterns:
                    continue

                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, temp_dir)
                dest_path = os.path.join(os.getcwd(), rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                if not os.path.exists(dest_path):
                    print(f"[NEW] Menambahkan file baru: {rel_path}")
                    shutil.copy2(src_path, dest_path)
                    added_count += 1
                else:
                    if not filecmp.cmp(src_path, dest_path, shallow=False):
                        if prompt_overwrite(dest_path, src_path, rel_path):
                            print(f"[UPDATE] Mengupdate: {rel_path}")
                            shutil.copy2(src_path, dest_path)
                            updated_count += 1
                        else:
                            print(f"[SKIP] Melewati: {rel_path}")
                            skipped_count += 1

    print("\n[OK] Proses update selesai!")
    print(
        f"Statistik: {added_count} ditambahkan, {updated_count} diupdate, {skipped_count} dilewati."
    )
    print(
        "Pastikan untuk mengecek perubahan, menjalankan `uv sync`, dan `python manage.py migrate` jika diperlukan."
    )


import json

from ..utils import get_project_manifest, is_rdp_project


def run_info(args: list[str]):
    """Menampilkan informasi apakah proyek ini dikenali sebagai proyek RDP."""
    manifest = get_project_manifest()
    if manifest:
        print("\n[OK] Proyek ini dikenali sebagai Proyek RDP Starter Kit.")
        print("-" * 40)
        print(f"  Tipe Proyek  : {manifest.get('project_type', 'rdp-starter-kit')}")

        # Ambil versi dari manifest, atau fallback ke baca pyproject.toml / config/version.json
        version = manifest.get("framework_version", "Tidak diketahui")
        print(f"  Versi RDP    : {version}")
        print(f"  Terdeteksi via: {manifest.get('_source', 'Unknown')}")
        print("-" * 40)
    else:
        print("\n[INFO] Proyek ini BUKAN proyek RDP Starter Kit atau belum diinisialisasi.")
        print("  Untuk mengubah proyek Django biasa menjadi RDP, jalankan: rdp init\n")


def run_init(args: list[str]):
    """Menginisialisasi proyek Django yang sudah ada menjadi proyek RDP."""
    if is_rdp_project():
        print("\n[INFO] Proyek ini sudah merupakan proyek RDP Starter Kit.")
        return

    print("\nMenginisialisasi proyek RDP Starter Kit...")

    # Deteksi apps_dir (default "apps")
    apps_dir = "apps"
    if not os.path.exists("apps"):
        print(
            "  [WARNING] Folder 'apps' tidak ditemukan. Pastikan Anda berada di root proyek Django."
        )

    # Coba tambahkan rdp.json sebagai marker proyek
    manifest = {
        "project_type": "rdp-starter-kit",
        "schema_version": 1,
        "framework_version": "0.6.2",
        "config": {
            "apps_dir": apps_dir,
            "settings_file": "config/settings/base.py",
            "urls_file": "config/urls.py",
        },
    }

    try:
        with open("rdp.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
        print("\n[OK] File rdp.json berhasil dibuat!")
        print(
            "Sekarang Anda dapat menggunakan perintah generator RDP (seperti `rdp new app`, `rdp new crud`, dll) di proyek ini."
        )
    except Exception as e:
        print(f"\n[ERROR] Gagal membuat rdp.json: {e}")
