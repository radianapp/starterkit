#!/usr/bin/env bash
# bin/upgrade-version.sh
# Bump versi CLI, commit, tag, dan push ke GitHub.
#
# Penggunaan:
#   bash bin/upgrade-version.sh          # interaktif — suggest versi berikutnya
#   bash bin/upgrade-version.sh 0.4.0   # langsung set versi
#
# Alur:
#   1. Ambil versi lokal dari pyproject.toml
#   2. Fetch versi terbaru dari GitHub (jika beda, tampilkan peringatan)
#   3. Suggest Mayor/Minor/Patch dari versi GitHub
#   4. Konfirmasi lalu bump, commit, tag, push

set -euo pipefail

PYPROJECT_RAW="https://raw.githubusercontent.com/radianapp/starterkit/main/pyproject.toml"

if [[ ! -f "pyproject.toml" || ! -f "scripts/rdp_cli.py" ]]; then
    echo "[ERROR] Jalankan dari root direktori project."
    exit 1
fi

# ── Versi lokal ───────────────────────────────────────────────────────────────
LOCAL=$(grep -m1 '^version' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# ── Versi GitHub ──────────────────────────────────────────────────────────────
echo "Mengambil versi terbaru dari GitHub..."
GITHUB=$(curl -sf --max-time 5 "$PYPROJECT_RAW" \
    | grep -m1 '^version' \
    | sed 's/version = "\(.*\)"/\1/') || GITHUB=""

if [[ -z "$GITHUB" ]]; then
    echo "[WARNING] Tidak bisa fetch versi dari GitHub. Pakai versi lokal sebagai acuan."
    GITHUB="$LOCAL"
fi

# ── Parse MAJOR.MINOR.PATCH dari GITHUB ──────────────────────────────────────
IFS='.' read -r MAJOR MINOR PATCH <<< "$GITHUB"

SUGGEST_PATCH="$MAJOR.$MINOR.$((PATCH + 1))"
SUGGEST_MINOR="$MAJOR.$((MINOR + 1)).0"
SUGGEST_MAJOR="$((MAJOR + 1)).0.0"

echo ""
echo "  Versi lokal   : $LOCAL"
echo "  Versi GitHub  : $GITHUB"
echo ""
echo "  Pilih tipe bump:"
echo "    1. Patch  — bug fix, tidak ada API baru         → $SUGGEST_PATCH"
echo "    2. Minor  — fitur baru, backward-compatible     → $SUGGEST_MINOR"
echo "    3. Major  — breaking change                     → $SUGGEST_MAJOR"
echo "    4. Manual — ketik sendiri"
echo ""

# Jika versi sudah diberikan lewat argumen, skip prompt
if [[ -n "${1:-}" ]]; then
    NEW_VERSION="$1"
else
    read -rp "  Pilih (1/2/3/4): " CHOICE
    case "$CHOICE" in
        1) NEW_VERSION="$SUGGEST_PATCH" ;;
        2) NEW_VERSION="$SUGGEST_MINOR" ;;
        3) NEW_VERSION="$SUGGEST_MAJOR" ;;
        4) read -rp "  Versi baru (x.y.z): " NEW_VERSION ;;
        *) echo "[ERROR] Pilihan tidak valid."; exit 1 ;;
    esac
fi

if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "[ERROR] Format versi harus x.y.z"
    exit 1
fi

echo ""
echo "  $LOCAL → $NEW_VERSION"
read -rp "  Lanjut? (y/N) " confirm
[[ "${confirm,,}" == "y" ]] || { echo "Dibatalkan."; exit 0; }

# ── Bump ─────────────────────────────────────────────────────────────────────
sed -i "s/^version = \"$LOCAL\"/version = \"$NEW_VERSION\"/" pyproject.toml
echo "[OK] pyproject.toml -> $NEW_VERSION"

sed -i "s/__version__ = \"$LOCAL\"/__version__ = \"$NEW_VERSION\"/" scripts/rdp_cli.py
echo "[OK] scripts/rdp_cli.py -> $NEW_VERSION"

git add pyproject.toml scripts/rdp_cli.py
git commit -m "chore(release): bump version to v$NEW_VERSION"
echo "[OK] Committed"

git tag "v$NEW_VERSION"
echo "[OK] Tagged v$NEW_VERSION"

git push origin main --tags
echo ""
echo "[OK] v$NEW_VERSION tersedia di GitHub."
echo "     User upgrade: uv tool upgrade rdp-starter-kit"
