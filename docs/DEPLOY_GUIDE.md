# Panduan Deployment & Manajemen RDP Framework

Dokumen ini menjelaskan cara menggunakan skrip interaktif yang disediakan untuk membantu proses pengembangan, pengujian, dan perilisan (deployment) dari RDP Framework.

Skrip alat bantu ini tersedia dalam dua versi:
- `bin/deploy.ps1` (Untuk pengguna Windows / PowerShell)
- `bin/deploy.sh` (Untuk pengguna Linux / macOS / WSL)

## Cara Menjalankan

**Untuk Windows (PowerShell):**
Buka terminal dan pastikan Anda berada di root direktori proyek, lalu jalankan:
```powershell
.\bin\deploy.ps1
```

**Untuk Linux / macOS / WSL (Bash):**
Pastikan skrip memiliki izin eksekusi (biasanya cukup dilakukan sekali), lalu jalankan:
```bash
chmod +x bin/deploy.sh
./bin/deploy.sh
```

## Fitur dan Penjelasan Menu

Saat dijalankan, skrip akan menampilkan antarmuka berbasis menu interaktif. Berikut adalah penjelasan untuk setiap opsi:

### 1. Jalankan Unit Tests (Pytest)
Opsi ini akan menjalankan seluruh rangkaian pengujian (*unit tests*) menggunakan `uv run pytest`. Selalu pastikan semua pengujian lulus (*passed*) sebelum Anda menaikkan versi atau mendistribusikan kode.

### 2. Manajemen Versi (Cek, Naikkan Versi, Tag & Rilis)
Opsi ini mengotomatisasi proses perilisan versi baru dari framework secara berurutan:
1. Skrip akan membaca versi saat ini dari file `pyproject.toml`.
2. Anda akan diminta memasukkan versi rilis yang baru (contoh: `0.2.0`).
3. Skrip mencari dan mengganti string versi di `pyproject.toml` secara otomatis.
4. Skrip akan memberikan konfirmasi untuk membuat *Git Commit* standar rilis (`chore: bump version to X.X.X`) beserta pembuatan *Git Tag* (contoh: `v0.2.0`).
5. Skrip akan memberikan konfirmasi akhir untuk langsung mendorong pembaruan (`git push origin main` dan `git push origin vX.X.X`) ke GitHub.

**⚠️ Praktik Terbaik (*Best Practice*) Sebelum Menaikkan Versi:**
Pastikan *working directory* Anda berstatus bersih (tidak ada *uncommitted changes*). Selesaikan pekerjaan Anda terlebih dahulu:
```bash
git add .
git commit -m "feat: menambahkan sistem X"
```
Setelah fitur/perbaikan tersimpan, barulah jalankan skrip ini dan pilih menu **Manajemen Versi**. Ini akan membuat riwayat *commit* menjadi rapi dan khusus terfokus pada rilisan versi tersebut.

### 3. CI/CD & Build Paket
Menu ini berisi petunjuk informasi mengenai pipeline otomatis (seperti GitHub Actions) dan memberikan Anda opsi untuk membungkus kode menjadi paket Python distribusi lokal (`sdist` dan `wheel`). Paket hasil bentukan akan tersimpan di dalam folder `dist/`. Ini berguna sebelum mendistribusikannya ke index package seperti PyPI.

### 4. Info Git & Deploy
Pintasan praktis untuk memeriksa status Git tanpa keluar dari antarmuka menu. Menu ini akan mencetak:
- Lokasi asal repositori jarak jauh (*Remote URL*).
- Cabang (*Branch*) yang sedang Anda gunakan.
- Laporan ringkas tentang file yang dimodifikasi (`git status -s`).

### 5. Perintah RDP CLI
Menu pembungkus (*wrapper*) untuk memanggil utilitas baris perintah dari ekosistem RDP, termasuk:
- `rdp init <nama>`: Menginisiasi proyek baru (Scaffolding).
- `rdp add <komponen>`: Menyuntikkan komponen UI Cotton (seperti modal, form, datatable) ke dalam *workspace* pengguna.
- `rdp serve`: Menjalankan aplikasi *development server*.

---
*(Catatan: Segala ketergantungan diwajibkan menggunakan ekosistem `uv` demi konsistensi. Jika ada error, pastikan environment Python virtual telah diaktifkan).*
