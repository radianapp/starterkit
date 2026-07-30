# bin/cli-version.ps1
# Bump versi CLI, commit, tag, dan push ke GitHub.
#
# Penggunaan:
#   .\bin\cli-version.ps1           # interaktif — suggest versi berikutnya
#   .\bin\cli-version.ps1 0.4.0    # langsung set versi
#
# Alur:
#   1. Ambil versi lokal dari pyproject.toml
#   2. Fetch versi terbaru dari GitHub (jika beda, tampilkan peringatan)
#   3. Suggest Mayor/Minor/Patch dari versi GitHub
#   4. Konfirmasi lalu bump, commit, tag, push

param(
    [string]$NewVersion = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$PyprojectRaw = "https://raw.githubusercontent.com/radianapp/starterkit/main/pyproject.toml"

if (-not (Test-Path "pyproject.toml") -or -not (Test-Path "scripts/rdp_cli.py")) {
    Write-Error "[ERROR] Jalankan dari root direktori project."
    exit 1
}

# ── Versi lokal ───────────────────────────────────────────────────────────────
$localMatch = Select-String -Path "pyproject.toml" -Pattern '^version = "(.+)"' | Select-Object -First 1
$local = $localMatch.Matches[0].Groups[1].Value

# ── Versi GitHub ──────────────────────────────────────────────────────────────
Write-Host "Mengambil versi terbaru dari GitHub..."
$github = $local  # fallback
try {
    $raw = (Invoke-WebRequest -Uri $PyprojectRaw -TimeoutSec 5 -UseBasicParsing).Content
    $ghMatch = [regex]::Match($raw, '^version = "(.+)"', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($ghMatch.Success) { $github = $ghMatch.Groups[1].Value }
} catch {
    Write-Host "[WARNING] Tidak bisa fetch versi dari GitHub. Pakai versi lokal sebagai acuan."
}

# ── Parse MAJOR.MINOR.PATCH ──────────────────────────────────────────────────
$parts  = $github.Split('.')
$major  = [int]$parts[0]
$minor  = [int]$parts[1]
$patch  = [int]$parts[2]

$suggestPatch = "$major.$minor.$($patch + 1)"
$suggestMinor = "$major.$($minor + 1).0"
$suggestMajor = "$($major + 1).0.0"

Write-Host ""
Write-Host "  Versi lokal   : $local"
Write-Host "  Versi GitHub  : $github"
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
Write-Host "  $local -> $NewVersion"
$confirm = Read-Host "  Lanjut? (y/N)"
if ($confirm.ToLower() -ne "y") {
    Write-Host "Dibatalkan."
    exit 0
}

# ── Bump ─────────────────────────────────────────────────────────────────────
(Get-Content "pyproject.toml") -replace "^version = `"$local`"", "version = `"$NewVersion`"" |
    Set-Content "pyproject.toml" -Encoding UTF8
Write-Host "[OK] pyproject.toml -> $NewVersion"

(Get-Content "scripts/rdp_cli.py") -replace "__version__ = `"$local`"", "__version__ = `"$NewVersion`"" |
    Set-Content "scripts/rdp_cli.py" -Encoding UTF8
Write-Host "[OK] scripts/rdp_cli.py -> $NewVersion"

git add pyproject.toml scripts/rdp_cli.py
git commit -m "chore(release): bump version to v$NewVersion"
Write-Host "[OK] Committed"

git tag "v$NewVersion"
Write-Host "[OK] Tagged v$NewVersion"

git push origin main "v$NewVersion"
Write-Host ""
Write-Host "[OK] v$NewVersion tersedia di GitHub."
Write-Host "     User upgrade: uv tool upgrade rdp-starter-kit"
