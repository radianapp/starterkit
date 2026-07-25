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

---

*Dokumentasi ini berlaku untuk RDP CLI v0.2.0+*
