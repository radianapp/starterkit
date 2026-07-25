#!/usr/bin/env bash
# install.sh — RDP StarterKit CLI installer untuk Linux/macOS
#
# Penggunaan:
#   curl -fsSL https://raw.githubusercontent.com/radianapp/starterkit/main/install.sh | bash
#
# Yang dilakukan script ini:
#   1. Cek OS (Linux/macOS)
#   2. Install uv jika belum ada
#   3. Install CLI `rdp` via uv tool install
#   4. Verifikasi instalasi

set -euo pipefail

# ── Konstanta ─────────────────────────────────────────────────────────────────
REPO="git+https://github.com/radianapp/starterkit.git"
PACKAGE="rdp-starter-kit"
CLI_NAME="rdp"
RDP_GREEN="\033[0;32m"
RDP_YELLOW="\033[1;33m"
RDP_RED="\033[0;31m"
RDP_CYAN="\033[0;36m"
RDP_BOLD="\033[1m"
RDP_RESET="\033[0m"

# ── Helpers ───────────────────────────────────────────────────────────────────
info()    { echo -e "${RDP_CYAN}[RDP]${RDP_RESET} $*"; }
success() { echo -e "${RDP_GREEN}[OK]${RDP_RESET}  $*"; }
warn()    { echo -e "${RDP_YELLOW}[WARN]${RDP_RESET} $*"; }
error()   { echo -e "${RDP_RED}[ERR]${RDP_RESET}  $*" >&2; exit 1; }

# ── Banner ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${RDP_BOLD}╔══════════════════════════════════════╗${RDP_RESET}"
echo -e "${RDP_BOLD}║   RDP StarterKit — CLI Installer     ║${RDP_RESET}"
echo -e "${RDP_BOLD}╚══════════════════════════════════════╝${RDP_RESET}"
echo ""

# ── Cek OS ────────────────────────────────────────────────────────────────────
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="Linux" ;;
    Darwin*) PLATFORM="macOS" ;;
    *)       error "OS tidak didukung: $OS. Gunakan Linux atau macOS." ;;
esac
info "Platform: $PLATFORM"

# ── Cek atau install uv ───────────────────────────────────────────────────────
if command -v uv &>/dev/null; then
    UV_VERSION="$(uv --version 2>/dev/null | awk '{print $2}')"
    success "uv sudah ada (v${UV_VERSION})"
else
    warn "uv belum terinstall — menginstall sekarang..."
    curl -fsSL https://astral.sh/uv/install.sh | sh

    # Tambah uv ke PATH untuk sesi ini
    export PATH="$HOME/.local/bin:$PATH"
    export PATH="$HOME/.cargo/bin:$PATH"

    if ! command -v uv &>/dev/null; then
        error "Instalasi uv gagal. Install manual: https://docs.astral.sh/uv/getting-started/installation/"
    fi
    success "uv berhasil diinstall"
fi

# ── Install rdp via uv tool ───────────────────────────────────────────────────
info "Menginstall CLI '${CLI_NAME}' dari ${REPO}..."
echo ""

if uv tool install "${REPO}" --force --refresh 2>&1; then
    echo ""
    success "CLI '${CLI_NAME}' berhasil diinstall!"
else
    echo ""
    error "Instalasi gagal. Coba manual: uv tool install ${REPO}"
fi

# ── Pastikan ~/.local/bin ada di PATH ─────────────────────────────────────────
UV_BIN_DIR="$HOME/.local/bin"
if [[ ":$PATH:" != *":${UV_BIN_DIR}:"* ]]; then
    warn "'${UV_BIN_DIR}' belum ada di PATH."
    echo ""
    echo "  Tambahkan baris berikut ke ~/.bashrc atau ~/.zshrc:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "  Lalu jalankan: source ~/.bashrc  (atau restart terminal)"
    echo ""
    # Coba tambah otomatis ke shell config
    SHELL_RC=""
    if [[ -n "${ZSH_VERSION:-}" ]] || [[ "$SHELL" == */zsh ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -n "${BASH_VERSION:-}" ]] || [[ "$SHELL" == */bash ]]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [[ -n "$SHELL_RC" ]]; then
        LINE='export PATH="$HOME/.local/bin:$PATH"'
        if ! grep -qF "$LINE" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# RDP StarterKit CLI" >> "$SHELL_RC"
            echo "$LINE" >> "$SHELL_RC"
            info "PATH ditambahkan ke $SHELL_RC — jalankan: source $SHELL_RC"
        fi
    fi
    export PATH="${UV_BIN_DIR}:$PATH"
fi

# ── Verifikasi ────────────────────────────────────────────────────────────────
echo ""
if command -v "${CLI_NAME}" &>/dev/null; then
    RDP_VERSION="$("${CLI_NAME}" --version 2>/dev/null || echo '(versi tidak diketahui)')"
    success "Verifikasi: ${RDP_VERSION}"
else
    warn "'rdp' belum bisa dipanggil di sesi ini."
    info "Jalankan 'source ~/.bashrc' atau buka terminal baru, lalu coba 'rdp --help'."
fi

# ── Selesai ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${RDP_BOLD}Mulai project baru:${RDP_RESET}"
echo ""
echo "    rdp new nama-project-saya"
echo ""
echo -e "${RDP_CYAN}Dokumentasi:${RDP_RESET} https://github.com/radianapp/starterkit"
echo ""
