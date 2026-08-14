#!/bin/bash
# ==============================================================================
# RDP Framework — Docker Compose Production & SSL Setup Script
# Mengotomatisasi: Docker check -> .env setup -> SSL Certbot -> Docker Compose Build & Run
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}===============================================================${NC}"
echo -e "${BLUE}   RDP Starter Kit — Docker Compose Production & SSL Setup     ${NC}"
echo -e "${BLUE}===============================================================${NC}"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# 1. Cek Docker dan Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker belum terpasang di sistem ini.${NC}"
    echo -e "Silakan pasang Docker terlebih dahulu: https://docs.docker.com/engine/install/"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo -e "${RED}[ERROR] Docker Compose plugin belum terpasang.${NC}"
    exit 1
fi

# 2. Input Parameter Konfigurasi
echo -e "\n${YELLOW}--- 1. Parameter Konfigurasi Production ---${NC}"

read -p "Domain / Subdomain Aplikasi (misal: app.example.com): " DOMAIN_NAME
while [[ -z "$DOMAIN_NAME" ]]; do
    echo -e "${RED}Domain wajib diisi untuk konfigurasi Nginx dan SSL!${NC}"
    read -p "Domain / Subdomain Aplikasi (misal: app.example.com): " DOMAIN_NAME
done

read -p "Email Administrator untuk Notifikasi SSL Let's Encrypt: " SSL_EMAIL
while [[ -z "$SSL_EMAIL" ]]; do
    echo -e "${RED}Email wajib diisi untuk Let's Encrypt SSL!${NC}"
    read -p "Email Administrator untuk Notifikasi SSL Let's Encrypt: " SSL_EMAIL
done

read -p "Database User [default: rdpuser]: " DB_USER
DB_USER="${DB_USER:-rdpuser}"

read -p "Database Password [default: $(openssl rand -hex 12)]: " DB_PASSWORD
DB_PASSWORD="${DB_PASSWORD:-$(openssl rand -hex 12)}"

read -p "Database Name [default: rdp_db]: " DB_NAME
DB_NAME="${DB_NAME:-rdp_db}"

# 3. Konfigurasi file .env
echo -e "\n${YELLOW}--- 2. Mempersiapkan File .env Production ---${NC}"
if [[ ! -f .env ]]; then
    if [[ -f .env.example ]]; then
        cp .env.example .env
    else
        touch .env
    fi
fi

# Update / Tambah variabel penting ke .env
export SECRET_KEY="${SECRET_KEY:-$(openssl rand -base64 32)}"
export DB_USER="$DB_USER"
export DB_PASSWORD="$DB_PASSWORD"
export DB_NAME="$DB_NAME"
export DOMAIN_NAME="$DOMAIN_NAME"
export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}"
export CACHE_URL="redis://redis:6379/0"

# Update konfigurasi .env
sed -i '/^DEBUG=/d' .env || true
sed -i '/^ALLOWED_HOSTS=/d' .env || true
sed -i '/^CSRF_TRUSTED_ORIGINS=/d' .env || true
sed -i '/^DATABASE_URL=/d' .env || true
sed -i '/^CACHE_URL=/d' .env || true

echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=${DOMAIN_NAME},localhost,web" >> .env
echo "CSRF_TRUSTED_ORIGINS=https://${DOMAIN_NAME}" >> .env
echo "DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}" >> .env
echo "CACHE_URL=redis://redis:6379/0" >> .env
echo "DB_USER=${DB_USER}" >> .env
echo "DB_PASSWORD=${DB_PASSWORD}" >> .env
echo "DB_NAME=${DB_NAME}" >> .env

chmod 600 .env
echo -e "${GREEN}✓ File .env berhasil dikonfigurasi secara aman (permission 600).${NC}"

# 4. Konfigurasi Nginx dengan Domain Target
echo -e "\n${YELLOW}--- 3. Menyiapkan Konfigurasi Nginx & Template SSL ---${NC}"
mkdir -p nginx certbot/conf certbot/www logs

# Ganti ${DOMAIN_NAME} pada file nginx/nginx.conf
sed -i "s/\${DOMAIN_NAME}/$DOMAIN_NAME/g" nginx/nginx.conf

# 5. Dummy SSL Certificate (Agar Nginx bisa start pertama kali sebelum Certbot memvalidasi)
CERT_DIR="certbot/conf/live/${DOMAIN_NAME}"
if [[ ! -d "$CERT_DIR" ]]; then
    echo -e "${YELLOW}Membuat dummy SSL certificate sementara agar Nginx dapat aktif...${NC}"
    mkdir -p "$CERT_DIR"
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
        -keyout "$CERT_DIR/privkey.pem" \
        -out "$CERT_DIR/fullchain.pem" \
        -subj "/CN=localhost" 2>/dev/null
    DUMMY_CERT=true
else
    DUMMY_CERT=false
fi

# 6. Build dan Jalankan Docker Compose
echo -e "\n${YELLOW}--- 4. Membangun dan Menjalankan Docker Compose Stack ---${NC}"
docker compose -f docker-compose.prod.yml up -d --build

# 7. Request Sertifikat Asli dari Let's Encrypt jika menggunakan dummy
if [[ "$DUMMY_CERT" == "true" ]]; then
    echo -e "\n${YELLOW}--- 5. Mengajukan Sertifikat SSL Resmi dari Let's Encrypt ---${NC}"
    
    # Hapus dummy certificate
    rm -rf "certbot/conf/live/${DOMAIN_NAME}"
    rm -rf "certbot/conf/archive/${DOMAIN_NAME}"
    rm -rf "certbot/conf/renewal/${DOMAIN_NAME}.conf"

    # Jalankan certbot via Docker container
    docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
        certbot certonly --webroot -w /var/www/certbot \
        --email ${SSL_EMAIL} \
        -d ${DOMAIN_NAME} \
        --rsa-key-size 4096 \
        --agree-tos \
        --force-renewal \
        --non-interactive" certbot || {
        echo -e "${RED}[WARNING] Permintaan SSL Let's Encrypt gagal. Pastikan Domain ${DOMAIN_NAME} sudah mengarah (A record DNS) ke IP server ini!${NC}"
        echo -e "${YELLOW}Mengembalikan sertifikat sementara...${NC}"
        mkdir -p "$CERT_DIR"
        openssl req -x509 -nodes -newkey rsa:2048 -days 30 \
            -keyout "$CERT_DIR/privkey.pem" \
            -out "$CERT_DIR/fullchain.pem" \
            -subj "/CN=localhost" 2>/dev/null
    }

    # Reload Nginx untuk memuat sertifikat baru
    docker compose -f docker-compose.prod.yml exec nginx nginx -s reload || true
fi

echo -e "\n${GREEN}===============================================================${NC}"
echo -e "${GREEN}   ✓ Docker Compose Production Berhasil Dijalankan!            ${NC}"
echo -e "${GREEN}===============================================================${NC}"
echo -e "• URL Aplikasi       : https://${DOMAIN_NAME}"
echo -e "• Status Kontainer   : docker compose -f docker-compose.prod.yml ps"
echo -e "• Live Logs          : docker compose -f docker-compose.prod.yml logs -f"
echo -e "• Buat Superuser     : docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo -e "==============================================================="
echo -e "Untuk pembaruan rutin ke depan, jalankan:"
echo -e "${BLUE}  bash scripts/docker_deploy_prod.sh${NC}"
echo -e "===============================================================\n"
