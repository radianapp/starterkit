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

## Form HTMX Mengembalikan Status 422 (Unprocessable Entity)

**Masalah**: Tool monitoring atau log menampilkan error HTTP 422 saat submit form gagal.
**Solusi**: Ini **bukan bug server**, melainkan perilaku yang diharapkan pada arsitektur HTMX. Status 422 menandakan validasi form gagal dan Django mengembalikan potongan HTML fragment error agar HTMX dapat me-render pesan error di form tanpa reload halaman.

## Peringatan WhiteNoise "No directory at .../staticfiles/"

**Masalah**: Terminal menampilkan `UserWarning: No directory at: .../staticfiles/` saat menjalankan test atau server.
**Solusi**: Peringatan ini muncul jika perintah `collectstatic` belum dijalankan di environment lokal. Anda dapat mengabaikannya di mode development, atau jalankan perintah berikut untuk mengumpulkan aset static:
```bash
uv run python manage.py collectstatic --no-input
```

## Nginx Mengembalikan "502 Bad Gateway" di Production

**Masalah**: Browser menampilkan error 502 Bad Gateway setelah deploy ke server Linux.
**Solusi**:
1. Periksa apakah service Gunicorn sedang berjalan:
   ```bash
   sudo systemctl status <app_name>-gunicorn
   ```
2. Jika service gagal *start*, periksa log error:
   ```bash
   sudo journalctl -u <app_name>-gunicorn -n 50 --no-pager
   ```
3. Periksa hak akses socket unix `/run/<app_name>/gunicorn.sock`. Pastikan user `www-data` (Nginx) memiliki hak akses baca/tulis ke direktori `/run/<app_name>/`.

## Error "CSRF verification failed. Request aborted" di HTTPS

**Masalah**: Submit form atau login gagal dengan error 403 Forbidden CSRF saat diakses melalui domain HTTPS.
**Solusi**:
1. Pastikan domain Anda telah ditambahkan ke `CSRF_TRUSTED_ORIGINS` di file `.env`:
   ```ini
   CSRF_TRUSTED_ORIGINS=https://app.example.com,https://www.example.com
   ```
2. Pastikan Nginx meneruskan header `proxy_set_header X-Forwarded-Proto $scheme;` dan di Django `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` aktif.
3. Restart service Gunicorn: `sudo systemctl restart <app_name>-gunicorn`.


