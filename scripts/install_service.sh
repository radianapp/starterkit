#!/bin/bash
# ==============================================================================
# RDP Framework — Linux Production Service Installer
# Script untuk setup otomatis Gunicorn (systemd), Nginx Reverse Proxy, dan SSL (Certbot)
# ==============================================================================

set -euo pipefail

# Warna terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}   RDP Starter Kit — Linux Production Service Setup  ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# 1. Pastikan dijalankan di Linux dengan akses sudo/root
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo -e "${RED}[ERROR] Skrip ini dirancang untuk dijalankan di server Linux (Ubuntu/Debian/Rocky/CentOS).${NC}"
    exit 1
fi

if [[ $EUID -ne 0 ]]; then
    echo -e "${YELLOW}[INFO] Membutuhkan hak akses superuser (sudo) untuk mengonfigurasi systemd dan Nginx.${NC}"
    SUDO="sudo"
else
    SUDO=""
fi

# 2. Deteksi Lokasi Project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

DEFAULT_APP_NAME="$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_' '_')"
DEFAULT_USER="$(logname 2>/dev/null || echo "$USER")"

echo -e "\n${YELLOW}--- 1. Parameter Konfigurasi Aplikasi ---${NC}"
read -p "Nama Service Aplikasi [default: $DEFAULT_APP_NAME]: " APP_NAME
APP_NAME="${APP_NAME:-$DEFAULT_APP_NAME}"

read -p "User Sistem Linux pemilik proses [default: $DEFAULT_USER]: " APP_USER
APP_USER="${APP_USER:-$DEFAULT_USER}"

APP_GROUP="$(id -gn "$APP_USER" 2>/dev/null || echo "$APP_USER")"

read -p "Domain / Subdomain Aplikasi (misal: app.example.com): " APP_DOMAIN
while [[ -z "$APP_DOMAIN" ]]; do
    echo -e "${RED}Domain wajib diisi untuk konfigurasi Nginx dan SSL!${NC}"
    read -p "Domain / Subdomain Aplikasi (misal: app.example.com): " APP_DOMAIN
done

# Hitung jumlah worker Gunicorn yang ideal: (2 x Core) + 1
CPU_CORES=$(nproc 2>/dev/null || echo 2)
RECOMMENDED_WORKERS=$(( (CPU_CORES * 2) + 1 ))
read -p "Jumlah Gunicorn Worker [default: $RECOMMENDED_WORKERS]: " GUNICORN_WORKERS
GUNICORN_WORKERS="${GUNICORN_WORKERS:-$RECOMMENDED_WORKERS}"

# Opsi Celery Worker
read -p "Apakah ingin membuat systemd service untuk Celery Worker juga? (y/n) [default: n]: " SETUP_CELERY
SETUP_CELERY="${SETUP_CELERY:-n}"

echo -e "\n${YELLOW}--- 2. Memeriksa & Mempersiapkan Lingkungan ---${NC}"

# Pastikan folder logs dan staticfiles ada
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/staticfiles"
mkdir -p "$PROJECT_DIR/media"

# Pastikan file .env ada
if [[ ! -f "$PROJECT_DIR/.env" ]]; then
    if [[ -f "$PROJECT_DIR/.env.example" ]]; then
        echo -e "${YELLOW}File .env tidak ditemukan, menyalin dari .env.example...${NC}"
        cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
        chmod 600 "$PROJECT_DIR/.env"
    else
        echo -e "${RED}[ERROR] File .env tidak ditemukan! Silakan buat .env terlebih dahulu.${NC}"
        exit 1
    fi
fi

# Cek uv / python virtualenv
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}uv belum terpasang. Menginstall uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo -e "${GREEN}Menginstall dependensi Python via uv...${NC}"
uv sync --no-dev

# Tentukan path Python dan Gunicorn
VENV_DIR="$PROJECT_DIR/.venv"
if [[ ! -f "$VENV_DIR/bin/gunicorn" ]]; then
    echo -e "${YELLOW}Gunicorn belum terpasang di venv, menambahkan gunicorn...${NC}"
    uv add gunicorn
fi

PYTHON_BIN="$VENV_DIR/bin/python"
GUNICORN_BIN="$VENV_DIR/bin/gunicorn"

# Jalankan migrasi dan collectstatic
echo -e "${GREEN}Menjalankan migrasi database...${NC}"
uv run python manage.py migrate --noinput

echo -e "${GREEN}Mengumpulkan file statis (collectstatic)...${NC}"
uv run python manage.py collectstatic --noinput

# Set kepemilikan folder
$SUDO chown -R "$APP_USER:$APP_GROUP" "$PROJECT_DIR/logs" "$PROJECT_DIR/staticfiles" "$PROJECT_DIR/media"

echo -e "\n${YELLOW}--- 3. Membuat systemd Service untuk Gunicorn ---${NC}"

GUNICORN_SERVICE_FILE="/etc/systemd/system/${APP_NAME}-gunicorn.service"

$SUDO bash -c "cat <<EOF > $GUNICORN_SERVICE_FILE
[Unit]
Description=Gunicorn daemon for ${APP_NAME} (${APP_DOMAIN})
After=network.target

[Service]
Type=notify
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${PROJECT_DIR}
EnvironmentFile=${PROJECT_DIR}/.env
ExecStart=${GUNICORN_BIN} \\
    config.wsgi:application \\
    --workers ${GUNICORN_WORKERS} \\
    --bind unix:/run/${APP_NAME}/gunicorn.sock \\
    --access-logfile ${PROJECT_DIR}/logs/gunicorn-access.log \\
    --error-logfile ${PROJECT_DIR}/logs/gunicorn-error.log \\
    --timeout 90 \\
    --graceful-timeout 30
ExecReload=/bin/kill -s HUP \\\$MAINPID
KillMode=mixed
TimeoutStopSec=10
PrivateTmp=true
RuntimeDirectory=${APP_NAME}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

echo -e "${GREEN}✓ File service Gunicorn dibuat: $GUNICORN_SERVICE_FILE${NC}"

# Buat service Celery jika diminta
if [[ "$SETUP_CELERY" == "y" || "$SETUP_CELERY" == "Y" ]]; then
    CELERY_BIN="$VENV_DIR/bin/celery"
    CELERY_SERVICE_FILE="/etc/systemd/system/${APP_NAME}-celery.service"
    
    $SUDO bash -c "cat <<EOF > $CELERY_SERVICE_FILE
[Unit]
Description=Celery Worker for ${APP_NAME}
After=network.target redis-server.service

[Service]
Type=simple
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${PROJECT_DIR}
EnvironmentFile=${PROJECT_DIR}/.env
ExecStart=${CELERY_BIN} -A config worker --loglevel=INFO --logfile=${PROJECT_DIR}/logs/celery-worker.log
Restart=on-failure
RestartSec=5
RuntimeDirectory=${APP_NAME}

[Install]
WantedBy=multi-user.target
EOF"
    echo -e "${GREEN}✓ File service Celery dibuat: $CELERY_SERVICE_FILE${NC}"
fi

# Reload systemd
$SUDO systemctl daemon-reload
$SUDO systemctl enable "${APP_NAME}-gunicorn"
$SUDO systemctl restart "${APP_NAME}-gunicorn"

if [[ "$SETUP_CELERY" == "y" || "$SETUP_CELERY" == "Y" ]]; then
    $SUDO systemctl enable "${APP_NAME}-celery"
    $SUDO systemctl restart "${APP_NAME}-celery"
fi

echo -e "\n${YELLOW}--- 4. Membuat Konfigurasi Nginx Reverse Proxy ---${NC}"

NGINX_AVAILABLE="/etc/nginx/sites-available/${APP_NAME}"
NGINX_ENABLED="/etc/nginx/sites-enabled/${APP_NAME}"

# Cek apakah Nginx terpasang
if ! command -v nginx &> /dev/null; then
    echo -e "${YELLOW}Nginx belum terpasang. Menginstall Nginx...${NC}"
    $SUDO apt update && $SUDO apt install -y nginx
fi

$SUDO bash -c "cat <<EOF > $NGINX_AVAILABLE
upstream ${APP_NAME}_gunicorn {
    server unix:/run/${APP_NAME}/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name ${APP_DOMAIN};

    client_max_body_size 25M;

    # Static files dengan long-term caching
    location /static/ {
        alias ${PROJECT_DIR}/staticfiles/;
        expires 30d;
        add_header Cache-Control \"public, immutable\";
    }

    # Media files (user uploads)
    location /media/ {
        alias ${PROJECT_DIR}/media/;
    }

    # Block akses ke file sensitif
    location ~ /\\.(env|git|py|sqlite3) {
        deny all;
        return 404;
    }

    # Proxy ke Gunicorn WSGI
    location / {
        proxy_pass http://${APP_NAME}_gunicorn;
        proxy_set_header Host \\\$host;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\\$scheme;
        proxy_redirect off;
        proxy_read_timeout 90;
        proxy_connect_timeout 90;
    }
}
EOF"

echo -e "${GREEN}✓ Konfigurasi Nginx dibuat: $NGINX_AVAILABLE${NC}"

# Aktifkan site di Nginx
$SUDO ln -sf "$NGINX_AVAILABLE" "$NGINX_ENABLED"

# Uji konfigurasi Nginx
if $SUDO nginx -t; then
    $SUDO systemctl reload nginx
    echo -e "${GREEN}✓ Nginx berhasil di-reload.${NC}"
else
    echo -e "${RED}[ERROR] Konfigurasi Nginx memiliki kesalahan sintaks. Periksa $NGINX_AVAILABLE.${NC}"
fi

echo -e "\n${YELLOW}--- 5. Opsi Konfigurasi SSL (Let's Encrypt / Certbot) ---${NC}"
read -p "Apakah Anda ingin langsung memasang SSL gratis via Certbot sekarang? (y/n) [default: y]: " INSTALL_SSL
INSTALL_SSL="${INSTALL_SSL:-y}"

if [[ "$INSTALL_SSL" == "y" || "$INSTALL_SSL" == "Y" ]]; then
    if ! command -v certbot &> /dev/null; then
        echo -e "${YELLOW}Certbot belum terpasang. Menginstall Certbot Nginx plugin...${NC}"
        $SUDO apt update && $SUDO apt install -y certbot python3-certbot-nginx
    fi

    echo -e "${GREEN}Menjalankan Certbot untuk domain ${APP_DOMAIN}...${NC}"
    $SUDO certbot --nginx -d "$APP_DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email || {
        echo -e "${YELLOW}Certbot otomatis membutuhkan prompt email atau DNS domain sudah menunjuk ke IP server ini.${NC}"
        echo -e "${YELLOW}Anda dapat menjalankan certbot manual nanti: sudo certbot --nginx -d $APP_DOMAIN${NC}"
    }
fi

echo -e "\n${GREEN}=====================================================${NC}"
echo -e "${GREEN}   Setup Production Selesai! Detail Informasi:       ${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo -e "• Service Gunicorn  : ${APP_NAME}-gunicorn.service"
echo -e "• Status Service    : sudo systemctl status ${APP_NAME}-gunicorn"
echo -e "• Socket Gunicorn   : /run/${APP_NAME}/gunicorn.sock"
echo -e "• Log Akses         : ${PROJECT_DIR}/logs/gunicorn-access.log"
echo -e "• Log Error         : ${PROJECT_DIR}/logs/gunicorn-error.log"
echo -e "• Domain Aplikasi   : http://${APP_DOMAIN} (atau https://${APP_DOMAIN})"
echo -e "• Nginx Config      : ${NGINX_AVAILABLE}"
echo -e "====================================================="
echo -e "Untuk update deployment berkala berikutnya, jalankan:"
echo -e "${BLUE}  bash scripts/deploy_prod.sh ${APP_NAME}${NC}"
echo -e "=====================================================\n"
