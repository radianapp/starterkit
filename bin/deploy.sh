#!/bin/bash

# Pindah ke root proyek
cd "$(dirname "$0")/.." || exit 1

# Fungsi untuk mengekstrak versi saat ini
get_current_version() {
    if [ -f "pyproject.toml" ]; then
        grep -E "^version = " pyproject.toml | awk -F'"' '{print $2}'
    else
        echo "0.0.0"
    fi
}

bump_version() {
    current_version=$(get_current_version)
    echo "Versi saat ini: $current_version"
    read -p "Masukkan versi baru (contoh: 0.2.0): " new_version
    
    if [ -z "$new_version" ]; then
        echo "Versi tidak boleh kosong."
        return
    fi
    
    # Update pyproject.toml
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
    else
        sed -i "s/^version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
    fi
    
    echo "Versi di pyproject.toml telah diperbarui ke $new_version"
    
    read -p "Apakah Anda ingin melakukan git commit dan membuat tag v$new_version sekarang? (y/n) " do_commit
    if [[ "$do_commit" == "y" || "$do_commit" == "Y" ]]; then
        git add pyproject.toml
        git commit -m "chore: bump version to $new_version"
        git tag "v$new_version"
        echo "Berhasil di-commit dan ditambahkan tag v$new_version."
        read -p "Push ke GitHub origin main & tags? (y/n) " do_push
        if [[ "$do_push" == "y" || "$do_push" == "Y" ]]; then
            git push origin main
            git push origin "v$new_version"
            echo "Pembaruan versi telah di-push!"
        fi
    fi
}

rdp_cli_menu() {
    echo "--- RDP CLI Commands ---"
    echo "1) rdp init <nama_proyek>"
    echo "2) rdp add <komponen>"
    echo "3) rdp serve"
    read -p "Pilih menu CLI rdp: " cli_choice
    case $cli_choice in
        1)
            read -p "Masukkan nama proyek: " proj_name
            echo "Menjalankan: rdp init $proj_name"
            # Tempat mengeksekusi rdp init sebenarnya:
            # uv run rdp init $proj_name
            ;;
        2)
            read -p "Masukkan nama komponen (misal: modal): " comp_name
            echo "Menjalankan: rdp add $comp_name"
            # Tempat mengeksekusi rdp add:
            # uv run rdp add $comp_name
            ;;
        3)
            echo "Menjalankan: rdp serve"
            # Tempat mengeksekusi rdp serve:
            # uv run rdp serve
            ;;
        *)
            echo "Pilihan tidak valid."
            ;;
    esac
}

while true; do
    echo ""
    echo "============================================="
    echo " RDP Framework Deployment & Management Tool  "
    echo "============================================="
    echo "1) Jalankan Unit Tests (Pytest)"
    echo "2) Manajemen Versi (Cek, Naikkan Versi, Tag & Rilis)"
    echo "3) CI/CD & Build Paket"
    echo "4) Info Git & Deploy"
    echo "5) Perintah RDP CLI"
    echo "0) Keluar"
    echo "============================================="
    read -p "Pilih menu [0-5]: " choice

    case $choice in
        1)
            echo "Menjalankan uv run pytest..."
            uv run pytest
            ;;
        2)
            bump_version
            ;;
        3)
            echo "--- CI/CD & Build Paket ---"
            echo "Pembangunan diotomatisasi melalui GitHub Actions (jika dikonfigurasi)."
            echo "Untuk mem-build paket Python secara lokal (sdist & wheel):"
            read -p "Apakah Anda ingin mem-build paket sekarang? (y/n) " do_build
            if [[ "$do_build" == "y" || "$do_build" == "Y" ]]; then
                uv pip install build
                python -m build
                echo "Paket telah di-build di folder dist/"
            fi
            ;;
        4)
            echo "--- Info Git & Deploy ---"
            git remote -v
            echo ""
            echo "Branch saat ini:"
            git branch --show-current
            echo ""
            echo "Status:"
            git status -s
            ;;
        5)
            rdp_cli_menu
            ;;
        0)
            echo "Keluar..."
            exit 0
            ;;
        *)
            echo "Pilihan tidak valid, coba lagi."
            ;;
    esac
done
