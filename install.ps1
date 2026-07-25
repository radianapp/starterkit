# install.ps1 — RDP StarterKit CLI installer untuk Windows (PowerShell)
#
# Penggunaan:
#   iex (irm https://raw.githubusercontent.com/radianapp/starterkit/main/install.ps1)
#
# Yang dilakukan script ini:
#   1. Cek PowerShell versi (minimal 5.1)
#   2. Install uv jika belum ada
#   3. Install CLI `rdp` via uv tool install
#   4. Tambah uv tools dir ke PATH jika belum ada
#   5. Verifikasi instalasi

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Konstanta ─────────────────────────────────────────────────────────────────
$REPO        = "git+https://github.com/radianapp/starterkit.git"
$CLI_NAME    = "rdp"

# ── Helpers ───────────────────────────────────────────────────────────────────
function Write-Info    { param($msg) Write-Host "[RDP] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[OK]  $msg" -ForegroundColor Green }
function Write-Warn    { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err     { param($msg) Write-Host "[ERR]  $msg" -ForegroundColor Red; exit 1 }

# ── Banner ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   RDP StarterKit — CLI Installer     ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Cek PowerShell ────────────────────────────────────────────────────────────
Write-Info "Platform: Windows (PowerShell $($PSVersionTable.PSVersion))"

# ── Cek atau install uv ───────────────────────────────────────────────────────
$uvCmd = Get-Command "uv" -ErrorAction SilentlyContinue
if ($uvCmd) {
    $uvVersion = (uv --version 2>$null) -replace "uv ", ""
    Write-Success "uv sudah ada (v$uvVersion)"
} else {
    Write-Warn "uv belum terinstall — menginstall sekarang..."

    try {
        # Installer resmi uv untuk Windows
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    } catch {
        Write-Err "Gagal install uv: $_`nInstall manual: https://docs.astral.sh/uv/getting-started/installation/"
    }

    # Refresh PATH di sesi ini
    $uvCargoPath = "$env:USERPROFILE\.cargo\bin"
    $uvLocalPath = "$env:USERPROFILE\.local\bin"
    $env:PATH = "$uvCargoPath;$uvLocalPath;$env:PATH"

    $uvCmd = Get-Command "uv" -ErrorAction SilentlyContinue
    if (-not $uvCmd) {
        Write-Err "uv tidak ditemukan setelah install. Buka terminal baru dan coba lagi."
    }
    Write-Success "uv berhasil diinstall"
}

# ── Install rdp via uv tool ───────────────────────────────────────────────────
Write-Info "Menginstall CLI '$CLI_NAME' dari $REPO..."
Write-Host ""

try {
    uv tool install $REPO --force
    Write-Host ""
    Write-Success "CLI '$CLI_NAME' berhasil diinstall!"
} catch {
    Write-Host ""
    Write-Err "Instalasi gagal: $_`nCoba manual: uv tool install $REPO"
}

# ── Tambah uv tools dir ke PATH permanen jika belum ada ──────────────────────
# uv tool install taruh binary di: %USERPROFILE%\.local\bin  (atau via uv home)
$uvToolsDir = ""
try {
    $uvToolsDir = (uv tool dir 2>$null).Trim()
} catch {}

if (-not $uvToolsDir) {
    $uvToolsDir = "$env:USERPROFILE\.local\bin"
}

$currentUserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentUserPath -notlike "*$uvToolsDir*") {
    Write-Warn "'$uvToolsDir' belum ada di PATH user — menambahkan sekarang..."
    $newPath = "$uvToolsDir;$currentUserPath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    $env:PATH = "$uvToolsDir;$env:PATH"
    Write-Success "PATH diupdate — berlaku di terminal baru"
} else {
    $env:PATH = "$uvToolsDir;$env:PATH"
}

# ── Verifikasi ────────────────────────────────────────────────────────────────
Write-Host ""
$rdpCmd = Get-Command $CLI_NAME -ErrorAction SilentlyContinue
if ($rdpCmd) {
    try {
        $rdpVersion = & $CLI_NAME --version 2>$null
        Write-Success "Verifikasi: $rdpVersion"
    } catch {
        Write-Success "CLI '$CLI_NAME' terinstall di: $($rdpCmd.Source)"
    }
} else {
    Write-Warn "'rdp' belum bisa dipanggil di sesi ini."
    Write-Info "Buka terminal PowerShell baru, lalu coba: rdp --help"
}

# ── Selesai ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Mulai project baru:" -ForegroundColor White
Write-Host ""
Write-Host "    rdp new nama-project-saya" -ForegroundColor Yellow
Write-Host ""
Write-Host "Dokumentasi: https://github.com/radianapp/starterkit" -ForegroundColor Cyan
Write-Host ""
