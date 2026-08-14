# Cookbook: Menghasilkan & Mengkustomisasi Dokumentasi ERD (Mermaid + Markdown)

Dokumen ini menjelaskan langkah demi langkah cara menggunakan dan mengotomatiskan fitur **ERD Analyzer & Generator** pada **RDP Starter Kit**.

---

## 🎯 Panduan Singkat

Setiap kali Anda menambahkan Model baru di folder `models/` atau mengubah bidang/relasi tabel, Anda **diwajibkan** untuk memperbarui dokumen ERD proyek.

Dengan perintah `generate_erd`, Anda tidak perlu lagi menggambar diagram ERD atau menulis tabel skema database secara manual.

---

## 🚀 Cara Penggunaan

### 1. Update Dokumentasi ERD Proyek Utama

Jalankan perintah berikut di root folder proyek:

```bash
uv run python manage.py generate_erd
```

Atau menggunakan CLI `rdp`:

```bash
rdp generate-erd
```

Perintah ini akan secara otomatis membaca semua model di aplikasi proyek (`accounts`, `dashboard`, `core`, `inventory`, dll.) dan memperbarui file **`docs/architecture/database.md`**.

---

### 2. Memfilter Aplikasi Tertentu

Jika Anda hanya ingin menghasilkan ERD untuk aplikasi domain bisnis tertentu (misal: modul `inventory` saja):

```bash
uv run python manage.py generate_erd --apps inventory --output docs/architecture/inventory_erd.md
```

---

### 3. Menampilkan Output Langsung ke Terminal (Preview)

Untuk melihat preview dokumen Markdown + Mermaid tanpa menyimpan ke file:

```bash
uv run python manage.py generate_erd --to-stdout
```

---

### 4. Menyesuaikan Judul Dokumen

```bash
uv run python manage.py generate_erd --title "Spesifikasi ERD Sistem Inventory & Pergudangan"
```

---

## 📐 Kompatibilitas Diagram Mermaid

Hasil ekspor diagram Mermaid menggunakan sintaks resmi `erDiagram`. Tipe relasi yang dipetakan secara otomatis:

- **One-to-One (`||--||`)**: Terdeteksi dari `OneToOneField`.
- **Foreign Key / One-to-Many (`||--o{`)**: Terdeteksi dari `ForeignKey`.
- **Many-to-Many (`}o--o{`)**: Terdeteksi dari `ManyToManyField`.

Diagram Mermaid ini dapat langsung di-render pada GitHub, VS Code (dengan ekstensi Markdown Preview Mermaid), maupun tools dokumentasi OpenAPI/Notion.
