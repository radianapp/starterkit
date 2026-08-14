# Referensi RDP CLI

RDP CLI (`rdp`) adalah alat baris perintah (*command-line interface*) untuk menyederhanakan pembuatan proyek baru berbasis RDP Starter Kit dari terminal, tanpa perlu meng-*clone* repositori secara manual.

---

## Instalasi

Instal CLI secara global menggunakan `uv tool` (hanya perlu dilakukan **satu kali**):

```bash
uv tool install git+https://github.com/radianapp/starterkit.git
```

Setelah instalasi selesai, perintah `rdp` akan tersedia secara global di sistem Anda dari folder mana pun.

**Prasyarat:**
- [uv](https://docs.astral.sh/uv/) sudah terinstal
- [Git](https://git-scm.com) sudah terinstal dan bisa diakses dari terminal
- Koneksi internet (untuk mengunduh template dari GitHub saat `rdp new`)

---

## Daftar Perintah

### `rdp new <nama-proyek>`

Bootstrap proyek Django baru dari template RDP secara interaktif.

**Penggunaan:**
```bash
rdp new portal-analytic
rdp new datahub-internal
```

**Wizard akan menanyakan:**
1. **Nama Proyek** -- dikonfirmasi dari argumen atau diisi ulang
2. **Deskripsi** -- deskripsi singkat proyek untuk `pyproject.toml`
3. **Warna Aksen** -- pilih dari: `teal`, `coral`, `purple`, `amber`, `gold`, `navy`
4. **Halaman Contact Us** -- halaman publik formulir kontak (opsional)
5. **Halaman FAQ** -- halaman publik pertanyaan umum (opsional)

**Apa yang dilakukan secara otomatis:**
- Meng-*clone* template terbaru dari [github.com/radianapp/starterkit](https://github.com/radianapp/starterkit.git)
- Menghapus riwayat `.git/` template agar proyek Anda bersih
- Men-*generate* `SECRET_KEY` baru yang aman secara acak
- Membuat file `.env` yang sudah dikonfigurasi (`SITE_NAME`, `RDP_APP_ACCENT`, dll)
- Memperbarui `pyproject.toml` dengan nama dan deskripsi proyek Anda
- Menambahkan *route* dan template HTML untuk halaman opsional yang dipilih

**Opsi Perintah:**
- `--local` / `-l` : Menggunakan folder starterkit lokal (cocok untuk pengujian lokal/offline tanpa `git clone` dari GitHub).

**Contoh Pengujian Lokal dari Source Code:**
```bash
# Jalankan langsung dari folder mana saja (PowerShell):
uv run python C:\Users\rahad\Work\org\rdp\beta\starterkit\scripts\rdp_cli.py new portal-analytic --local

# Atau via env variable:
$env:RDP_TEMPLATE_PATH="C:\path\to\starterkit"
uv run python C:\path\to\starterkit\scripts\rdp_cli.py new portal-analytic
```


**Langkah selanjutnya setelah wizard selesai:**
```bash
cd nama-proyek-anda
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py loaddemodata   # muat data sampel (opsional)
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Buka **http://localhost:8000** -- selesai!


---

### `rdp --version`

Tampilkan versi CLI yang terinstal.

```bash
rdp --version
# Output: rdp v0.2.0
```

---

### `rdp --help`

Tampilkan pesan bantuan dan daftar perintah yang tersedia.

```bash
rdp --help
rdp -h
```

---

### `rdp make-crud-codemap <app_label> <ModelName>`

Men-generate dokumen terpadu **Code Map**, **User Guide**, **FAQ**, dan **Help/Troubleshooting** secara otomatis untuk entity CRUD, serta mengupdate `docs/codemap/INDEX.md`.

```bash
rdp make-crud-codemap inventory Produk
```

---

### `rdp codemap`

Men-scan ulang seluruh file event di `docs/codemap/` dan meng-generate/update **Master Table of Contents (`docs/codemap/INDEX.md`)**.

```bash
rdp codemap
```

---

### `rdp generate-erd` / `rdp erd`

Menganalisis skema database berbasis Django Models dan menghasilkan dokumen ERD format Markdown lengkap dengan diagram Mermaid (`erDiagram`).

**Penggunaan:**
```bash
# Hasilkan dokumen ERD default ke docs/architecture/database.md
rdp generate-erd

# Filter aplikasi tertentu
rdp generate-erd --apps inventory,accounts

# Cetak langsung ke stdout terminal
rdp generate-erd --to-stdout

# Custom path output file
rdp generate-erd --output docs/erd-internal.md
```

**Opsi:**
- `--output` / `-o` : Path file Markdown tujuan (Default: `docs/architecture/database.md`)
- `--apps` / `-a` : Daftar nama app dipisahkan koma (contoh: `inventory,accounts`)
- `--exclude-apps` / `-e` : App yang dikecualikan
- `--to-stdout` : Cetak ke terminal tanpa menyimpan file
- `--title` : Judul kustom dokumen ERD

---

## Deteksi Proyek RDP & Kompatibilitas Proyek Existing

### 1. Sistem Signature Manifest (`rdp.json`) & Hierarki Fallback
Untuk memastikan deteksi proyek bersifat deterministik sekaligus menjaga **kompatibilitas penuh antar versi (backward compatibility)**, RDP CLI menggunakan sistem pembacaan signature berjenjang (*multi-tier fallback hierarchy*):

1. **Prioritas 1 — File Manifest Resmi (`rdp.json`)**:
   File signature di root proyek yang menyimpan metadata, versi skema, dan konfigurasi path modular:
   ```json
   {
     "$schema": "https://cdn.radian.web.id/schemas/rdp-manifest-v1.json",
     "project_type": "rdp-starter-kit",
     "schema_version": 1,
     "framework_version": "0.5.0",
     "config": {
       "apps_dir": "apps",
       "settings_file": "config/settings/base.py",
       "urls_file": "config/urls.py"
     }
   }
   ```
2. **Prioritas 2 — In-Tree Metadata di `pyproject.toml` (`[tool.rdp]`)**:
   Jika `rdp.json` tidak ada, CLI memeriksa blok `[tool.rdp]` di file `pyproject.toml`.
3. **Prioritas 3 — Fallback Heuristik Legacy (Proyek Versi v0.1 s/d v0.4.7)**:
   Jika kedua file signature di atas tidak ada, CLI tetap mengenali proyek lama dengan memeriksa keberadaan folder `apps/` dan `config/version.json` / `config/settings/base.py`.

Jika tidak ada satupun signature atau struktur yang cocok, CLI akan menandai direktori sebagai proyek non-RDP dan menampilkan panduan.


---

### 2. Apakah Proyek Django Existing (Non-RDP) Bisa Menggunakan RDP CLI?
**Bisa**, terbagi menjadi dua level fungsionalitas:
- **Perintah Django Wrapper (100% Kompatibel)**:
  Perintah seperti `rdp runserver` (atau `rdp r`), `rdp migrate`, `rdp makemigrations`, `rdp shell`, `rdp lint`, dan `rdp doctor` dapat langsung digunakan pada proyek Django standar mana pun selama memiliki file `manage.py`.
- **Perintah Generator & Scaffolding (Butuh Penyesuaian Struktur)**:
  Perintah seperti `rdp new app`, `rdp new crud`, `rdp new component`, `rdp new api`, dan `rdp make` membutuhkan proyek existing mengadopsi struktur konvensi RDP.

---

### 3. Potensi Konflik pada Proyek Existing Non-RDP & Cara Menghindarinya

| Area Potensi Konflik | Penyebab Konflik | Solusi & Cara Menghindari |
|---|---|---|
| **Lokasi Direktori App** | Django standar meletakkan app di root level (`./my_app`), sedangkan RDP di `./apps/my_app`. | Buat folder `apps/` dan letakkan aplikasi di dalamnya, atau tambahkan `sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))`. |
| **Injeksi Settings Otomatis** | RDP menginjeksi app baru ke list `LOCAL_APPS` di `config/settings/base.py`. | Buat struktur `config/settings/base.py` atau daftarkan app secara manual jika menggunakan `settings.py` standar. |
| **Template Engine (Django-Cotton)** | Generator RDP menghasilkan tag `<c-layout.app>` dan `<c-rdp.*>`. Jika `django_cotton` belum terpasang, Django template standar akan error. | Pasang package `django-cotton` via `uv add django-cotton` dan tambahkan ke `INSTALLED_APPS`. |
| **User Model & Auth Mixins** | RDP mengasumsikan `AUTH_USER_MODEL = "accounts.User"` untuk fitur profile & tenant. | Sesuaikan inheritance model atau gunakan default Django model dengan membatasi pemakaian fitur multi-tenant starterkit. |

---

## Memperbarui CLI

Untuk mendapatkan versi terbaru dari CLI:

```bash
uv tool upgrade rdp-starter-kit
```

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `rdp: command not found` | Pastikan `~/.local/bin` ada di `PATH` Anda, atau jalankan `uv tool update-shell` |
| `git: command not found` | Instal Git dari [git-scm.com](https://git-scm.com) |
| Error koneksi saat `rdp new` | Periksa koneksi internet Anda; repositori GitHub harus bisa diakses |
| Direktori sudah ada | Hapus folder target terlebih dahulu atau pilih nama proyek yang berbeda |
| `Direktori 'apps' tidak ditemukan` | Anda menjalankan perintah generator di luar proyek RDP. Pastikan berada di root direktori proyek. |

---

*Dokumentasi ini berlaku untuk RDP CLI v0.2.0+*

