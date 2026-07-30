# bin/app-version.ps1
# Bump versi khusus untuk Aplikasi (bukan Starter Kit), commit, dan tag.
#
# Penggunaan:
#   .\bin\app-version.ps1           # interaktif — suggest versi berikutnya
#   .\bin\app-version.ps1 1.0.1    # langsung set versi
#

param(
    [string]$NewVersion = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$VersionFile = "config/version.json"

if (-not (Test-Path "manage.py")) {
    Write-Error "[ERROR] Jalankan dari root direktori project (sejajar dengan manage.py)."
    exit 1
}

# ── Versi lokal ───────────────────────────────────────────────────────────────
$local = "1.0.0"
if (Test-Path $VersionFile) {
    $vData = Get-Content $VersionFile | ConvertFrom-Json
    if ($vData.version) {
        $local = $vData.version
    }
}

# ── Parse MAJOR.MINOR.PATCH ──────────────────────────────────────────────────
$parts  = $local.Split('.')
$major  = [int]$parts[0]
$minor  = [int]$parts[1]
$patch  = [int]$parts[2]

$suggestPatch = "$major.$minor.$($patch + 1)"
$suggestMinor = "$major.$($minor + 1).0"
$suggestMajor = "$($major + 1).0.0"

Write-Host ""
Write-Host "  App Version Saat Ini : $local"
Write-Host ""
Write-Host "  Pilih tipe bump:"
Write-Host "    1. Patch  -- bug fix, tidak ada fitur baru           -> $suggestPatch"
Write-Host "    2. Minor  -- fitur baru, backward-compatible         -> $suggestMinor"
Write-Host "    3. Major  -- breaking change                         -> $suggestMajor"
Write-Host "    4. Manual -- ketik sendiri"
Write-Host ""

if ($NewVersion -eq "") {
    $choice = Read-Host "  Pilih (1/2/3/4)"
    switch ($choice) {
        "1" { $NewVersion = $suggestPatch }
        "2" { $NewVersion = $suggestMinor }
        "3" { $NewVersion = $suggestMajor }
        "4" { $NewVersion = Read-Host "  Versi baru (x.y.z)" }
        default { Write-Error "[ERROR] Pilihan tidak valid."; exit 1 }
    }
}

if ($NewVersion -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "[ERROR] Format versi harus x.y.z"
    exit 1
}

Write-Host ""
Write-Host "  $local -> $NewVersion"
$confirm = Read-Host "  Lanjut? (y/N)"
if ($confirm.ToLower() -ne "y") {
    Write-Host "Dibatalkan."
    exit 0
}

Write-Host ""
$releaseNotes = Read-Host "  Keterangan / Release Notes (Opsional, misal: 'Fitur Dashboard Baru')"

# ── Dapatkan Informasi User & Waktu ──────────────────────────────────────────
$gitUser = "System"
try {
    $gitUser = (git config user.name).Trim()
} catch {
    Write-Host "[WARNING] Tidak bisa mendapatkan git user.name."
}

# Format ISO8601 dengan timezone
$currentDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"

# ── Update version.json ──────────────────────────────────────────────────────
$jsonObj = @{
    version = $NewVersion
    updated_at = $currentDate
    updated_by = $gitUser
    description = $releaseNotes
}
$jsonString = $jsonObj | ConvertTo-Json -Depth 2
Set-Content -Path $VersionFile -Value $jsonString -Encoding UTF8

Write-Host "[OK] $VersionFile diperbarui ke v$NewVersion"

# ── Konfirmasi Git Tag ───────────────────────────────────────────────────────
Write-Host ""
$gitConfirm = Read-Host "  Apakah Anda ingin commit dan buat Git Tag untuk rilis ini? (y/N)"
if ($gitConfirm.ToLower() -eq "y") {
    git add $VersionFile
    
    $commitMsg = "chore(release): bump app version to v$NewVersion"
    if ($releaseNotes -ne "") {
        $commitMsg = "$commitMsg`n`n$releaseNotes"
    }
    
    git commit -m $commitMsg
    Write-Host "[OK] Committed"

    if ($releaseNotes -ne "") {
        git tag -a "v$NewVersion" -m $releaseNotes
    } else {
        git tag "v$NewVersion"
    }
    Write-Host "[OK] Tagged v$NewVersion"

    Write-Host ""
    Write-Host "Jangan lupa push tag dengan perintah: git push origin main --tags"
} else {
    Write-Host "Pembuatan tag Git dilewati."
}

Write-Host "Selesai!"
