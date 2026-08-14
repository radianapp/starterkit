# Panduan Deployment & Manajemen RDP Framework

Dokumen ini menjelaskan cara menggunakan skrip interaktif yang disediakan untuk membantu proses pengembangan, pengujian, dan perilisan (deployment) dari RDP Framework.

Skrip alat bantu ini tersedia dalam dua versi:
- `bin/deploy.ps1` (Untuk pengguna Windows / PowerShell)
- `bin/deploy.sh` (Untuk pengguna Linux / macOS / WSL)

> **💡 Panduan Arsitektur & Opsi Hosting:** Untuk perbandingan lengkap antara Bare-Metal, Docker Compose, Self-Hosted PaaS (Coolify), Managed PaaS (Render/Railway), Serverless (Cloud Run), dan Kubernetes, lihat [Matriks Opsi Deployment](file:///docs/deployment/deployment-options-matrix.md).

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

### 6. Setup Linux Service (Gunicorn + Nginx + SSL)
Opsi otomatisasi untuk menginstal aplikasi sebagai daemon systemd Linux di balik reverse proxy Nginx dan mengonfigurasi SSL otomatis dengan Let's Encrypt / Certbot:
- Membuat service unit `/etc/systemd/system/<nama_service>-gunicorn.service`.
- Mengonfigurasi Nginx upstream unix socket dan static/media file caching.
- Menjalankan `migrate`, `collectstatic`, dan `certbot --nginx -d <domain>`.
- Panduan lengkap: [Panduan Setup Production Service](file:///docs/deployment/production-service-setup.md).

### 7. Deploy Pembaruan ke Production (Pull, Migrate, Restart)
Opsi otomatisasi pembaruan kode di server production dengan satu perintah:
- Mengambil commit terbaru dari git (`git pull origin main`).
- Sinkronisasi dependensi (`uv sync --no-dev`).
- Migrasi database (`python manage.py migrate --noinput`).
- Koleksi aset statis (`python manage.py collectstatic --noinput`).
- Restart service Gunicorn dan reload Nginx secara zero-downtime.

### 8. Setup Docker Compose Production & SSL (Let's Encrypt)
Opsi otomatisasi deployment berbasis kontainer Docker untuk lingkungan production:
- Membangun image Docker immutable multi-stage dengan Python 3.12 dan `uv`.
- Mengonfigurasi seluruh stack kontainer: Django Web (Gunicorn), Celery Worker & Beat, PostgreSQL 16, Redis 7, Nginx, dan Certbot.
- Memasang dan mengotomatisasi sertifikat SSL Let's Encrypt secara otomatis.
- Panduan lengkap: [Panduan Deployment Docker Compose Production](file:///docs/deployment/docker-compose-production.md).

### 9. Deploy Pembaruan Docker Production (Pull, Rebuild, Restart)
Opsi pembaruan kontainer production dengan satu perintah:
- Mengambil commit terbaru (`git pull`).
- Membangun ulang dan me-restart kontainer `web` dan `celery` tanpa mengganggu database dan redis (`docker compose up -d --build`).
- Membersihkan image lama yang tidak terpakai (`docker image prune`).

---
*(Catatan: Segala ketergantungan diwajibkan menggunakan ekosistem `uv` demi konsistensi. Jika ada error, pastikan environment Python virtual telah diaktifkan).*


