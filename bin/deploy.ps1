<#
.SYNOPSIS
RDP Framework Deployment & Management Tool
#>

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path "$ScriptPath\.."

function Get-CurrentVersion {
    if (Test-Path "pyproject.toml") {
        $content = Get-Content "pyproject.toml"
        foreach ($line in $content) {
            if ($line -match '^version\s*=\s*"(.*)"') {
                return $matches[1]
            }
        }
    }
    return "0.0.0"
}

function Bump-Version {
    $currentVersion = Get-CurrentVersion
    Write-Host "Versi saat ini: $currentVersion" -ForegroundColor Yellow
    $newVersion = Read-Host "Masukkan versi baru (contoh: 0.2.0)"
    
    if ([string]::IsNullOrWhiteSpace($newVersion)) {
        Write-Host "Versi tidak boleh kosong." -ForegroundColor Red
        return
    }
    
    $content = Get-Content "pyproject.toml"
    $newContent = $content -replace "^version\s*=\s*`"$currentVersion`"", "version = `"$newVersion`""
    Set-Content -Path "pyproject.toml" -Value $newContent -Encoding UTF8
    
    Write-Host "Versi di pyproject.toml telah diperbarui ke $newVersion" -ForegroundColor Green
    
    $doCommit = Read-Host "Apakah Anda ingin melakukan git commit dan membuat tag v$newVersion sekarang? (y/n)"
    if ($doCommit -match '^[yY]') {
        git add pyproject.toml
        git commit -m "chore: bump version to $newVersion"
        git tag "v$newVersion"
        Write-Host "Berhasil di-commit dan ditambahkan tag v$newVersion." -ForegroundColor Green
        
        $doPush = Read-Host "Push ke GitHub origin main & tags? (y/n)"
        if ($doPush -match '^[yY]') {
            git push origin main
            git push origin "v$newVersion"
            Write-Host "Pembaruan versi telah di-push!" -ForegroundColor Green
        }
    }
}

function Show-RdpCliMenu {
    Write-Host "--- RDP CLI Commands ---" -ForegroundColor Cyan
    Write-Host "1) rdp init <nama_proyek>"
    Write-Host "2) rdp add <komponen>"
    Write-Host "3) rdp serve"
    
    $cliChoice = Read-Host "Pilih menu CLI rdp"
    switch ($cliChoice) {
        "1" {
            $projName = Read-Host "Masukkan nama proyek"
            Write-Host "Menjalankan: rdp init $projName" -ForegroundColor Magenta
            # Tempat mengeksekusi rdp init sebenarnya:
            # uv run rdp init $projName
        }
        "2" {
            $compName = Read-Host "Masukkan nama komponen (misal: modal)"
            Write-Host "Menjalankan: rdp add $compName" -ForegroundColor Magenta
            # Tempat mengeksekusi rdp add:
            # uv run rdp add $compName
        }
        "3" {
            Write-Host "Menjalankan: rdp serve" -ForegroundColor Magenta
            # Tempat mengeksekusi rdp serve:
            # uv run rdp serve
        }
        default { Write-Host "Pilihan tidak valid." -ForegroundColor Red }
    }
}

do {
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host " RDP Framework Deployment & Management Tool  " -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "1) Jalankan Unit Tests (Pytest)"
    Write-Host "2) Manajemen Versi (Cek, Naikkan Versi, Tag & Rilis)"
    Write-Host "3) CI/CD & Build Paket"
    Write-Host "4) Info Git & Deploy"
    Write-Host "5) Perintah RDP CLI"
    Write-Host "0) Keluar"
    Write-Host "=============================================" -ForegroundColor Cyan
    
    $choice = Read-Host "Pilih menu [0-5]"
    
    switch ($choice) {
        "1" {
            Write-Host "Menjalankan uv run pytest..." -ForegroundColor Yellow
            uv run pytest
        }
        "2" {
            Bump-Version
        }
        "3" {
            Write-Host "--- CI/CD & Build Paket ---" -ForegroundColor Cyan
            Write-Host "Pembangunan diotomatisasi melalui GitHub Actions (jika dikonfigurasi)."
            $doBuild = Read-Host "Apakah Anda ingin mem-build paket Python (sdist & wheel) secara lokal sekarang? (y/n)"
            if ($doBuild -match '^[yY]') {
                uv pip install build
                python -m build
                Write-Host "Paket telah di-build di folder dist/" -ForegroundColor Green
            }
        }
        "4" {
            Write-Host "--- Info Git & Deploy ---" -ForegroundColor Cyan
            git remote -v
            Write-Host "`nBranch saat ini:" -ForegroundColor Yellow
            git branch --show-current
            Write-Host "`nStatus:" -ForegroundColor Yellow
            git status -s
        }
        "5" {
            Show-RdpCliMenu
        }
        "0" {
            Write-Host "Keluar..." -ForegroundColor Yellow
            break
        }
        default {
            Write-Host "Pilihan tidak valid, coba lagi." -ForegroundColor Red
        }
    }
} while ($choice -ne "0")
