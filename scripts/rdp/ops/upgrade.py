# scripts/rdp/ops/upgrade.py
# US-024: CLI rdp — operasi upgrade (cli, packages, monitor, ai, plugin)

import subprocess

from ..utils import __version__, _fetch_latest_version, _parse_version


def run_upgrade(args):
    """Memeriksa pembaruan pustaka."""
    print("=" * 60)
    print("  Memeriksa pembaruan pustaka (Dependencies)...")
    print("=" * 60)
    try:
        subprocess.run(["uv", "pip", "list", "--outdated"], check=True)
        print("\n  [INFO] Jika ingin memperbarui, gunakan 'uv pip install --upgrade <package>'")
    except Exception:
        print("  [ERROR] Gagal menjalankan pengecekan uv pip list.")


def run_upgrade_cli(args):
    """
    TUJUAN: Upgrade binary CLI rdp ke versi terbaru dari GitHub.

    ALUR:
      1. Fetch versi terbaru dari GitHub
      2. Bandingkan dengan versi lokal
      3. Jalankan `uv tool upgrade rdp-starter-kit` jika ada update (atau --force)
      4. Paksa upgrade jika argumen --force diberikan

    DIPANGGIL DARI: main() via `rdp upgrade-cli`
    """
    force = "--force" in args

    print(f"  Versi lokal  : v{__version__}")

    latest = _fetch_latest_version()
    if latest:
        print(f"  Versi GitHub : v{latest}")
        if _parse_version(latest) <= _parse_version(__version__) and not force:
            print("\n  Sudah menggunakan versi terbaru.")
            print("  Gunakan --force untuk upgrade paksa: rdp upgrade-cli --force")
            return
    else:
        print("  Versi GitHub : (tidak bisa dicek — uv akan menentukan)")

    print("\nMenjalankan: uv tool upgrade rdp-starter-kit")
    try:
        subprocess.run(["uv", "tool", "upgrade", "rdp-starter-kit"], check=True)
        print("\n  [OK] CLI rdp berhasil diupgrade.")
        print("       Restart terminal jika versi belum berubah.")
    except subprocess.CalledProcessError:
        print("\n  [ERROR] Upgrade gagal. Pastikan CLI diinstall via:")
        print("          uv tool install git+https://github.com/radianapp/starterkit.git")
    except FileNotFoundError:
        print("\n  [ERROR] Perintah 'uv' tidak ditemukan. Install dari https://docs.astral.sh/uv/")


def run_monitor(args):
    """Menampilkan status monitoring sistem dasar."""
    import shutil as _shutil

    print("=" * 60)
    print("  RDP Monitor (Status Sistem)")
    print("=" * 60)
    total, used, free = _shutil.disk_usage("/")
    print(f"Disk Total : {total // (2**30)} GiB")
    print(f"Disk Used  : {used // (2**30)} GiB")
    print(f"Disk Free  : {free // (2**30)} GiB")
    print(
        "\n[INFO] Untuk monitoring yang lebih lengkap, jalankan utilitas seperti 'htop' atau 'glances'."
    )


def run_ai(args):
    """Placeholder untuk fitur AI assistant."""
    print("=" * 60)
    print("  RDP AI Assistant")
    print("=" * 60)
    if args:
        prompt = " ".join(args)
        print(f"\nPrompt: '{prompt}'\n")
    print("🤖 [COMING SOON] Modul RDP AI sedang dalam tahap pengembangan.")
    print(
        "Nantinya, Anda cukup memberikan prompt dan CLI akan merancang struktur direktori, model, view, hingga HTMX secara ajaib!"
    )


def run_plugin(args):
    """Placeholder untuk sistem plugin."""
    print("=" * 60)
    print("  RDP Plugin System")
    print("=" * 60)
    if args and args[0] == "install":
        plugin_name = args[1] if len(args) > 1 else "<nama-plugin>"
        print(f"📦 Menginstal plugin '{plugin_name}'...")
    print("\n[COMING SOON] Ekosistem plugin RDP sedang dirancang.")
    print(
        "Anda akan segera bisa menambahkan fungsionalitas kompleks seperti 'blog', 'ecommerce', atau 'auditlog' hanya dengan satu perintah."
    )
