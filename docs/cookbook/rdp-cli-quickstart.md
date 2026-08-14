# Panduan RDP CLI: Membuat Project Baru (Quickstart)

Dokumen ini berisi panduan *step-by-step* untuk menggunakan RDP CLI dalam membuat aplikasi baru. Panduan ini dirancang untuk mencapai *Success Metric* dari PRD v0.1 (Setup project baru selesai hingga `runserver` dalam < 5 menit).

Dalam contoh ini, kita akan membuat sebuah project baru bernama **FNB** dan mengaktifkan fitur halaman depan (Landing Page).

## Langkah 1: Menginisiasi Project & Menambah Halaman Depan

Kita menggunakan alat CLI interaktif `rdp new` yang secara otomatis akan:
1. Menentukan nama proyek (me-rename *starter kit*).
2. Cloning repositori versi template terbaru.
3. Mengatur *secret key* unik untuk project Anda.
4. Menyiapkan konfigurasi *environment* awal (`.env`).

**Jalankan perintah ini di terminal:**

```bash
# 1. Pastikan RDP CLI sudah terinstal secara global menggunakan uv
uv tool install rdp-cli

# 2. Inisiasi project baru bernama FNB
rdp new FNB
```

Saat *wizard interaktif* berjalan, CLI akan menanyakan beberapa opsi. Untuk menambahkan halaman publik (seperti halaman depan, tentang kami, kontak), jawab dengan **Y**:

```text
> Apakah Anda ingin menambahkan Halaman Publik (Landing Page, About, Contact)? (y/N): Y
> Pilih warna aksen RDP-UI (default: zinc): (tekan enter untuk memilih default)
```

Setelah selesai, struktur aplikasi lengkap akan tersalin di dalam folder `./FNB/`.

## Langkah 2: Menyiapkan Lingkungan (Environment) & Database

Sesuai dengan **FR-01** pada spesifikasi PRD v0.1: 
*"Developer dapat clone repo starter kit dan menjalankan `uv run python manage.py runserver` tanpa langkah konfigurasi tambahan selain menyalin `.env.example` ke `.env`."*

Karena proses penyalinan `.env` sudah ditangani secara otomatis oleh RDP CLI di Langkah 1, Anda hanya perlu menjalankan instalasi library dan menyiapkan database awal:

```bash
# 1. Masuk ke dalam direktori project yang baru saja dibuat
cd FNB

# 2. Install / Sync semua dependency Python ke dalam virtual environment (menggunakan uv)
uv sync

# 3. Jalankan migrasi database awal (default: SQLite untuk development)
uv run python manage.py migrate
```

## Langkah 3: Menjalankan Server Development

Sekarang aplikasi siap dijalankan:

```bash
# Menggunakan command bawaan Django:
uv run python manage.py runserver

# ATAU, menggunakan shortcut praktis dari RDP CLI:
rdp serve
```

## Hasil (Selesai dalam < 5 Menit!)

Buka *browser* Anda dan kunjungi `http://127.0.0.1:8000/`.
- Halaman pertama yang akan Anda lihat adalah **Landing Page / Halaman Depan** (ter-generate karena Anda menekan `Y` pada proses instalasi).
- Fitur *Authentication* utama seperti (Login, Register, Forgot Password, Reset) sudah langsung siap digunakan dan dapat diakses melalui tombol di pojok kanan atas Navigasi.
- Halaman Administrasi bisa diakses melalui URL `/admin/`.
