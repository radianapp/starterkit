# Help & Troubleshooting

## UI Tidak Ter-render dengan Benar
**Masalah**: Komponen form atau tombol tidak memiliki gaya CSS.
**Solusi**: Pastikan Anda sudah memuat file CSS utama RDP UI di template base Anda. Gunakan tag `{% static 'vendor/rdp-ui/rdp.css' %}` dan pastikan folder static disajikan dengan benar oleh server pengembangan.

## Komponen Cotton Tidak Dikenali
**Masalah**: Error template "Component 'c-rdp.button' does not exist".
**Solusi**: Pastikan `django-cotton` sudah ditambahkan di `INSTALLED_APPS` pada `settings/base.py`. Komponen RDP UI harus berada di direktori `templates/cotton/rdp/`.

## Versi Tidak Tampil di Sidebar / Changelog

**Masalah**: `{{ FRAMEWORK_VERSION }}` atau `{{ LOCAL_APP_VERSION }}` tidak tampil (kosong/blank).
**Solusi**:
1. Pastikan variabel ada di file `.env` Anda:
   ```ini
   FRAMEWORK_VERSION=0.3.0
   LOCAL_APP_VERSION=1.0.0
   ```
2. Restart server Django (`CTRL+C` lalu `uv run manage.py runserver`). Perubahan `.env` tidak otomatis terdeteksi oleh `StatReloader`.
3. Pastikan `apps.core.context_processors.debug_settings` terdaftar di `TEMPLATES[0]['OPTIONS']['context_processors']` di `config/settings/base.py`.

## Halaman `/changelog/` Mengembalikan Error 404

**Masalah**: URL `/changelog/` tidak ditemukan.
**Solusi**: Pastikan URL sudah didaftarkan di `apps/dashboard/urls.py`:
```python
path("changelog/", views.SystemUpdateListView.as_view(), name="changelog"),
```
Dan pastikan `apps/dashboard/views/__init__.py` mengekspor `SystemUpdateListView`.

## Error Migrasi `dashboard.0003_systemupdate`

**Masalah**: Migrasi gagal dengan error `table already exists` atau `no module`.
**Solusi**: Jalankan secara berurutan:
```bash
uv run manage.py makemigrations dashboard
uv run manage.py migrate
```

## Bulk Upload User Tertunda atau Gagal

**Masalah**: Proses import user dari file CSV yang besar (>1000 baris) tidak masuk ke database atau stuck.
**Solusi**:
1. Pemrosesan >1000 baris dikerjakan di background oleh **Celery**. Pastikan *worker* Celery dan instance Redis sudah aktif.
2. Jalankan perintah `uv run celery -A config worker -l info` di terminal terpisah untuk menghidupkan Celery.
3. Cek log pada layar Celery tersebut untuk menemukan error spesifik pada format file CSV atau email server yang mungkin gagal terkirim.
