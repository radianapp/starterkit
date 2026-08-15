#!/bin/bash
# bin/version.sh
# Bump versi untuk keseluruhan RDP Starter Kit (CLI & App) secara bersamaan.
#
# Penggunaan:
#   ./bin/version.sh           # interaktif — suggest versi berikutnya
#   ./bin/version.sh 1.0.1     # langsung set versi
#

set -e

VERSION_JSON_FILE="config/version.json"
PYPROJECT_FILE="pyproject.toml"
CLI_FILE="scripts/rdp_cli.py"

if [ ! -f "manage.py" ]; then
    echo "[ERROR] Jalankan dari root direktori project (sejajar dengan manage.py)."
    exit 1
fi

# ── Versi saat ini (Source of Truth dari pyproject.toml) ────────────────────
CURRENT_VERSION=$(grep '^version = ' "$PYPROJECT_FILE" | head -n 1 | sed 's/version = "\(.*\)"/\1/')
if [ -z "$CURRENT_VERSION" ]; then
    CURRENT_VERSION="1.0.0"
fi

# ── Parse MAJOR.MINOR.PATCH ──────────────────────────────────────────────────
IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
if [ -z "$major" ] || [ -z "$minor" ] || [ -z "$patch" ]; then
    major=1
    minor=0
    patch=0
fi

suggestPatch="${major}.${minor}.$((patch + 1))"
suggestMinor="${major}.$((minor + 1)).0"
suggestMajor="$((major + 1)).0.0"

echo ""
echo "  Versi Saat Ini (Unified): $CURRENT_VERSION"
echo ""
echo "  Pilih tipe bump:"
echo "    1. Patch  -- bug fix, tidak ada API baru         -> $suggestPatch"
echo "    2. Minor  -- fitur baru, backward-compatible     -> $suggestMinor"
echo "    3. Major  -- breaking change                     -> $suggestMajor"
echo "    4. Manual -- ketik sendiri"
echo ""

NEW_VERSION=$1
if [ -z "$NEW_VERSION" ]; then
    read -p "  Pilih (1/2/3/4): " choice
    case $choice in
        1) NEW_VERSION=$suggestPatch ;;
        2) NEW_VERSION=$suggestMinor ;;
        3) NEW_VERSION=$suggestMajor ;;
        4) read -p "  Versi baru (x.y.z): " NEW_VERSION ;;
        *) echo "[ERROR] Pilihan tidak valid."; exit 1 ;;
    esac
fi

if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "[ERROR] Format versi harus x.y.z"
    exit 1
fi

echo ""
echo "  $CURRENT_VERSION -> $NEW_VERSION"
read -p "  Lanjut? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Dibatalkan."
    exit 0
fi

echo ""
read -p "  Keterangan / Release Notes (Opsional): " releaseNotes

# ── Dapatkan Informasi User & Waktu ──────────────────────────────────────────
gitUser="System"
if git config user.name > /dev/null 2>&1; then
    gitUser=$(git config user.name)
fi
currentDate=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ── Update Files ──────────────────────────────────────────────────────────────

# 1. Update config/version.json
cat > "$VERSION_JSON_FILE" <<EOF
{
  "version": "$NEW_VERSION",
  "updated_at": "$currentDate",
  "updated_by": "$gitUser",
  "description": "$releaseNotes"
}
EOF
echo "[OK] $VERSION_JSON_FILE -> v$NEW_VERSION"

# 2. Update pyproject.toml
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
    sed -i '' "s/^framework_version = \".*\"/framework_version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
else
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
    sed -i "s/^framework_version = \".*\"/framework_version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"
fi
echo "[OK] $PYPROJECT_FILE -> v$NEW_VERSION"

# 3. Update scripts/rdp_cli.py
if [ -f "$CLI_FILE" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" "$CLI_FILE"
    else
        sed -i "s/^__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" "$CLI_FILE"
    fi
    echo "[OK] $CLI_FILE -> v$NEW_VERSION"
fi

# ── Konfirmasi Git Tag ───────────────────────────────────────────────────────
echo ""
read -p "  Apakah Anda ingin commit dan buat Git Tag untuk rilis ini? (y/N): " gitConfirm
if [[ "$gitConfirm" =~ ^[Yy]$ ]]; then
    git add "$VERSION_JSON_FILE" "$PYPROJECT_FILE" "$CLI_FILE"
    
    commitMsg="chore(release): bump unified version to v$NEW_VERSION"
    if [ -n "$releaseNotes" ]; then
        commitMsg="$commitMsg

$releaseNotes"
    fi
    
    git commit -m "$commitMsg"
    echo "[OK] Committed"

    if [ -n "$releaseNotes" ]; then
        git tag -a "v$NEW_VERSION" -m "$releaseNotes"
    else
        git tag "v$NEW_VERSION"
    fi
    echo "[OK] Tagged v$NEW_VERSION"

    echo ""
    echo "Jangan lupa push tag dengan perintah: git push origin main --tags"
else
    echo "Pembuatan tag Git dilewati."
fi

echo "Selesai!"
