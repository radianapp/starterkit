# Memulai Penggunaan (Getting Started)
<!-- US: US-023 — Dokumentasi project -->

Panduan ini membantu Anda melakukan setup awal dan menjalankan RDP Starter Kit di mesin lokal Anda dalam waktu kurang dari 5 menit.

## Persyaratan Sistem

Sebelum memulai, pastikan mesin Anda telah terpasang perkakas berikut:
- **Python >= 3.11**
- **Git**
- **uv** (Package manager yang direkomendasikan). Untuk memasang `uv`, jalankan perintah berikut:
  - **macOS / Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - **Windows**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

---

## Langkah 1: Clone Repository

Clone repository starter kit ke folder lokal Anda:

```bash
git clone <repository-url> my-rdp-project
cd my-rdp-project
```

---

## Langkah 2: Setup Environment & Dependensi

Salin file template environment variable:

```bash
cp .env.example .env
```

Gunakan `uv` untuk membuat virtual environment dan menginstal semua dependensi secara otomatis:

```bash
uv sync
```

---

## Langkah 3: Jalankan Migrasi Database

Jalankan perintah berikut untuk menginisialisasi SQLite database lokal dan menerapkan migrasi awal:

```bash
uv run python manage.py migrate
```

---

## Langkah 4: Buat Superuser (Admin)

Buat akun superuser untuk mengakses panel admin Django:

```bash
uv run python manage.py createsuperuser
```

---

## Langkah 5: Jalankan Server Lokal

Nyalakan server development Django:

```bash
uv run python manage.py runserver
```

Buka peramban (browser) Anda dan akses alamat berikut:
- **Halaman Utama / Dashboard**: [http://localhost:8000](http://localhost:8000)
- **Django Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Langkah 6: Jalankan Pengujian (Opsional)

Untuk memastikan seluruh pengujian berjalan dengan baik di lokal Anda, jalankan unit test menggunakan pytest:

```bash
uv run pytest
```
