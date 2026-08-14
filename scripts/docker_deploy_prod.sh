#!/bin/bash
# ==============================================================================
# RDP Framework — Fast Docker Production Update Script
# Git Pull -> Docker Build -> Container Restart (Zero / Near Zero Downtime)
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}===============================================================${NC}"
echo -e "${BLUE}   RDP Starter Kit — Docker Compose Production Update Deploy   ${NC}"
echo -e "${BLUE}===============================================================${NC}"

# 1. Ambil update kode terbaru
echo -e "\n${YELLOW}[1/3] Mengambil commit terbaru dari repository (git pull)...${NC}"
git pull origin main || git pull

# 2. Rebuild dan restart kontainer web & celery
echo -e "\n${YELLOW}[2/3] Membangun ulang dan me-restart container (web, celery)...${NC}"
docker compose -f docker-compose.prod.yml up -d --build --no-deps web celery_worker celery_beat

# 3. Bersihkan image lama yang tidak terpakai
echo -e "\n${YELLOW}[3/3] Membersihkan dangling images lama...${NC}"
docker image prune -f

echo -e "\n${GREEN}===============================================================${NC}"
echo -e "${GREEN}   ✓ Pembaruan Docker Production Selesai dengan Sukses!        ${NC}"
echo -e "${GREEN}===============================================================${NC}"
