#!/bin/bash
# bin/app-version.sh
# Bump versi khusus untuk Aplikasi (bukan Starter Kit), commit, dan tag.
#
# Penggunaan:
#   ./bin/app-version.sh           # interaktif — suggest versi berikutnya
#   ./bin/app-version.sh 1.0.1     # langsung set versi
#

set -e

VERSION_FILE="config/version.json"

if [ ! -f "manage.py" ]; then
    echo "[ERROR] Jalankan dari root direktori project (sejajar dengan manage.py)."
    exit 1
fi

# ── Versi lokal ───────────────────────────────────────────────────────────────
LOCAL_VER="1.0.0"
if [ -f "$VERSION_FILE" ]; then
    # Parse version sederhana dengan grep
    EXTRACTED=$(grep -o '"version": "[^"]*' "$VERSION_FILE" | grep -o '[^"]*$')
    if [ ! -z "$EXTRACTED" ]; then
        LOCAL_VER="$EXTRACTED"
    fi
fi

# ── Parse MAJOR.MINOR.PATCH ──────────────────────────────────────────────────
IFS='.' read -r major minor patch <<< "$LOCAL_VER"

SUGGEST_PATCH="${major}.${minor}.$((patch + 1))"
SUGGEST_MINOR="${major}.$((minor + 1)).0"
SUGGEST_MAJOR="$((major + 1)).0.0"

echo ""
echo "  App Version Saat Ini : $LOCAL_VER"
echo ""

NEW_VER=$1

if [ -z "$NEW_VER" ]; then
    echo "  Pilih tipe bump:"
    echo "    1. Patch  -- bug fix, tidak ada fitur baru           -> $SUGGEST_PATCH"
    echo "    2. Minor  -- fitur baru, backward-compatible         -> $SUGGEST_MINOR"
    echo "    3. Major  -- breaking change                         -> $SUGGEST_MAJOR"
    echo "    4. Manual -- ketik sendiri"
    echo ""
    read -p "  Pilih (1/2/3/4): " choice

    case $choice in
        1) NEW_VER=$SUGGEST_PATCH ;;
        2) NEW_VER=$SUGGEST_MINOR ;;
        3) NEW_VER=$SUGGEST_MAJOR ;;
        4) read -p "  Versi baru (x.y.z): " NEW_VER ;;
        *) echo "[ERROR] Pilihan tidak valid."; exit 1 ;;
    esac
fi

if ! [[ "$NEW_VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "[ERROR] Format versi harus x.y.z"
    exit 1
fi

echo ""
echo "  $LOCAL_VER -> $NEW_VER"
read -p "  Lanjut? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Dibatalkan."
    exit 0
fi

echo ""
read -p "  Keterangan / Release Notes (Opsional, misal: 'Fitur Dashboard Baru'): " RELEASE_NOTES

# ── Dapatkan Informasi User & Waktu ──────────────────────────────────────────
GIT_USER=$(git config user.name || echo "System")
CURRENT_DATE=$(date +"%Y-%m-%dT%H:%M:%S%z") # ISO8601 like

# ── Update version.json ──────────────────────────────────────────────────────
cat > "$VERSION_FILE" <<EOF
{
  "version": "$NEW_VER",
  "updated_at": "$CURRENT_DATE",
  "updated_by": "$GIT_USER",
  "description": "$RELEASE_NOTES"
}
EOF

echo "[OK] $VERSION_FILE diperbarui ke v$NEW_VER"

# ── Konfirmasi Git Tag ───────────────────────────────────────────────────────
echo ""
read -p "  Apakah Anda ingin commit dan buat Git Tag untuk rilis ini? (y/N): " git_confirm
if [[ "$git_confirm" =~ ^[Yy]$ ]]; then
    git add "$VERSION_FILE"
    
    if [ -n "$RELEASE_NOTES" ]; then
        git commit -m "chore(release): bump app version to v$NEW_VER" -m "$RELEASE_NOTES"
    else
        git commit -m "chore(release): bump app version to v$NEW_VER"
    fi
    echo "[OK] Committed"

    if [ -n "$RELEASE_NOTES" ]; then
        git tag -a "v$NEW_VER" -m "$RELEASE_NOTES"
    else
        git tag "v$NEW_VER"
    fi
    echo "[OK] Tagged v$NEW_VER"

    echo ""
    echo "Jangan lupa push tag dengan perintah: git push origin main --tags"
else
    echo "Pembuatan tag Git dilewati."
fi

echo "Selesai!"
