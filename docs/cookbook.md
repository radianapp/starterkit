# RDP Cookbook (Kumpulan Resep Teknis)
<!-- US: US-023 — Dokumentasi project -->

Cookbook ini berisi instruksi praktis untuk melakukan perluasan fitur dan arsitektur pada RDP Starter Kit.

---

## 1. Menambahkan Django App Baru (Struktur Package)

RDP Starter Kit mewajibkan pembuatan Django App dalam bentuk **Struktur Package Terpisah** untuk setiap fungsinya, bukan file datar (`models.py`, `views.py` langsung).

Langkah-langkah pembuatan:
1. Buat folder app baru di dalam folder `apps/`, misalnya `apps/billing/`.
2. Buat file `apps/billing/apps.py` dengan isi konfigurasi aplikasi Django.
3. Buat struktur package internal:
   - `apps/billing/models/__init__.py`
   - `apps/billing/views/__init__.py`
   - `apps/billing/services/__init__.py`
   - `apps/billing/forms/__init__.py`
   - `apps/billing/admin/__init__.py`
4. Pastikan Anda mengimpor kelas-kelas publik dari sub-file ke file `__init__.py` masing-masing agar Django dapat memuatnya dengan benar.
5. Daftarkan app Anda ke `LOCAL_APPS` di [config/settings/base.py](file:///c:/Users/rahad/Work/org/rdp/beta/starterkit/config/settings/base.py#L182-L186).

---

## 2. Mengaktifkan Celery untuk Background Tasks

Celery digunakan untuk memproses task secara asynchronous (misal: mengirim email, batch processing).

1. Pastikan dependensi `celery` and `redis` telah terinstall (sudah ada di `pyproject.toml` starter kit).
2. Buat file konfigurasi Celery di `config/celery.py`:
   ```python
   import os
   from celery import Celery

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
   app = Celery('rdp_project')
   app.config_from_object('django.conf:settings', namespace='CELERY')
   app.autodiscover_tasks()
   ```
3. Tambahkan konfigurasi Redis broker di `config/settings/base.py`:
   ```python
   CELERY_BROKER_URL = env_var("REDIS_URL", "redis://localhost:6379/0")
   CELERY_RESULT_BACKEND = env_var("REDIS_URL", "redis://localhost:6379/0")
   ```
4. Jalankan worker Celery menggunakan perintah:
   ```bash
   uv run celery -A config worker -l info
   ```

---

## 3. Mengaktifkan ASGI / WebSocket

Untuk komunikasi real-time, Anda dapat beralih menggunakan ASGI server (Channels).

1. Install `channels` ke project Anda:
   ```bash
   uv add channels[daphne]
   ```
2. Daftarkan `daphne` di bagian teratas `INSTALLED_APPS` sebelum `staticfiles`.
3. Buat file `config/asgi.py`:
   ```python
   import os
   from django.core.asgi import get_asgi_application
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.auth import AuthMiddlewareStack

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": AuthMiddlewareStack(
           URLRouter(
               # Masukkan routing WebSocket app di sini
           )
       ),
   })
   ```
4. Ganti konfigurasi ASGI_APPLICATION di settings base.

---

## 4. Menggunakan AWS S3 / Cloudflare R2 untuk Media Storage

Secara default, media files disimpan secara lokal. Untuk deployment multi-server, Anda harus menyimpan media di S3-compatible storage.

1. Install dependensi `django-storages` dan `boto3`:
   ```bash
   uv add django-storages boto3
   ```
2. Tambahkan variabel lingkungan berikut ke `.env`:
   ```env
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_ENDPOINT_URL=https://your-endpoint.com  # Opsional untuk R2/MinIO
   ```
3. Sesuaikan konfigurasi media storage di `settings/production.py`:
   ```python
   STORAGES = {
       "default": {
           "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
       },
       "staticfiles": {
           "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
       },
   }
   ```
