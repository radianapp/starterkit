# bin/version.ps1
# Bump versi untuk keseluruhan RDP Starter Kit (CLI & App) secara bersamaan.
#
# Penggunaan:
#   .\bin\version.ps1           # interaktif — suggest versi berikutnya
#   .\bin\version.ps1 1.0.1     # langsung set versi
#

param(
    [string]$NewVersion = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$VersionJsonFile = "config/version.json"
$PyprojectFile = "pyproject.toml"
$CliFile = "scripts/rdp_cli.py"

if (-not (Test-Path "manage.py")) {
    Write-Error "[ERROR] Jalankan dari root direktori project (sejajar dengan manage.py)."
    exit 1
}

# ── Versi saat ini (Source of Truth dari pyproject.toml) ────────────────────
$localMatch = Select-String -Path $PyprojectFile -Pattern '^version = "(.+)"' | Select-Object -First 1
$currentVersion = "1.0.0"
if ($localMatch) {
    $currentVersion = $localMatch.Matches[0].Groups[1].Value
}

# ── Parse MAJOR.MINOR.PATCH ──────────────────────────────────────────────────
$parts  = $currentVersion.Split('.')
if ($parts.Length -eq 3) {
    $major  = [int]$parts[0]
    $minor  = [int]$parts[1]
    $patch  = [int]$parts[2]
} else {
    $major = 1; $minor = 0; $patch = 0
}

$suggestPatch = "$major.$minor.$($patch + 1)"
$suggestMinor = "$major.$($minor + 1).0"
$suggestMajor = "$($major + 1).0.0"

Write-Host ""
Write-Host "  Versi Saat Ini (Unified): $currentVersion"
Write-Host ""
Write-Host "  Pilih tipe bump:"
Write-Host "    1. Patch  -- bug fix, tidak ada API baru         -> $suggestPatch"
Write-Host "    2. Minor  -- fitur baru, backward-compatible     -> $suggestMinor"
Write-Host "    3. Major  -- breaking change                     -> $suggestMajor"
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
Write-Host "  $currentVersion -> $NewVersion"
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
$currentDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"

# ── Update Files ──────────────────────────────────────────────────────────────

# 1. Update config/version.json
$jsonObj = @{
    version = $NewVersion
    updated_at = $currentDate
    updated_by = $gitUser
    description = $releaseNotes
}
$jsonString = $jsonObj | ConvertTo-Json -Depth 2
Set-Content -Path $VersionJsonFile -Value $jsonString -Encoding UTF8
Write-Host "[OK] $VersionJsonFile -> v$NewVersion"

# 2. Update pyproject.toml (version dan framework_version)
$pyContent = Get-Content $PyprojectFile
$pyContent = $pyContent -replace '^version = ".*"', "version = `"$NewVersion`""
$pyContent = $pyContent -replace '^framework_version = ".*"', "framework_version = `"$NewVersion`""
Set-Content -Path $PyprojectFile -Value $pyContent -Encoding UTF8
Write-Host "[OK] $PyprojectFile -> v$NewVersion"

# 3. Update scripts/rdp_cli.py
if (Test-Path $CliFile) {
    $cliContent = Get-Content $CliFile
    $cliContent = $cliContent -replace '__version__ = ".*"', "__version__ = `"$NewVersion`""
    Set-Content -Path $CliFile -Value $cliContent -Encoding UTF8
    Write-Host "[OK] $CliFile -> v$NewVersion"
}

# ── Konfirmasi Git Tag ───────────────────────────────────────────────────────
Write-Host ""
$gitConfirm = Read-Host "  Apakah Anda ingin commit dan buat Git Tag untuk rilis ini? (y/N)"
if ($gitConfirm.ToLower() -eq "y") {
    git add $VersionJsonFile $PyprojectFile $CliFile
    
    $commitMsg = "chore(release): bump unified version to v$NewVersion"
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
