#!/bin/bash
# ==============================================================================
# RDP Framework — Fast Production Deployment Update Script
# Menjalankan alur pembaruan: Git Pull -> uv sync -> Migrate -> Collectstatic -> Restart Service -> Health Check
# ==============================================================================

set -euo pipefail

# Warna terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

DEFAULT_APP_NAME="$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_' '_')"
APP_NAME="${1:-$DEFAULT_APP_NAME}"

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}   RDP Starter Kit — Production Update Deployment    ${NC}"
echo -e "${BLUE}   Target Service: ${APP_NAME}-gunicorn              ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# 1. Git pull
echo -e "\n${YELLOW}[1/5] Mengambil update source code terbaru (git pull)...${NC}"
git pull origin main || git pull

# 2. Dependency sync via uv
echo -e "\n${YELLOW}[2/5] Mengupdate dependensi via uv...${NC}"
uv sync --no-dev

# 3. Database migrations
echo -e "\n${YELLOW}[3/5] Menjalankan migrasi database...${NC}"
uv run python manage.py migrate --noinput

# 4. Collect static files
echo -e "\n${YELLOW}[4/5] Mengumpulkan static assets (collectstatic)...${NC}"
uv run python manage.py collectstatic --noinput

# 5. Restart systemd services
echo -e "\n${YELLOW}[5/5] Me-restart service systemd...${NC}"
if systemctl is-active --quiet "${APP_NAME}-gunicorn"; then
    sudo systemctl restart "${APP_NAME}-gunicorn"
    echo -e "${GREEN}✓ Service ${APP_NAME}-gunicorn berhasil di-restart.${NC}"
else
    echo -e "${YELLOW}Service ${APP_NAME}-gunicorn belum aktif, mencoba menyalakan...${NC}"
    sudo systemctl start "${APP_NAME}-gunicorn" || true
fi

if systemctl is-active --quiet "${APP_NAME}-celery"; then
    sudo systemctl restart "${APP_NAME}-celery"
    echo -e "${GREEN}✓ Service ${APP_NAME}-celery berhasil di-restart.${NC}"
fi

# Reload Nginx jika ada perubahan static config
if command -v nginx &> /dev/null; then
    sudo systemctl reload nginx || true
fi

echo -e "\n${GREEN}=====================================================${NC}"
echo -e "${GREEN}   ✓ Deployment Pembaruan Selesai dengan Sukses!     ${NC}"
echo -e "${GREEN}=====================================================${NC}"
