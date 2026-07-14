# Cookbook: Konfigurasi Media Storage Cloud (AWS S3 atau GCS)

Resep ini menjelaskan cara memindahkan media storage lokal (SQLite/File System) ke Cloud Object Storage (seperti AWS S3 atau Google Cloud Storage) pada environment production.

---

## Langkah 1: Pasang Dependencies
Tambahkan library `django-storages` dan SDK client object storage (misalnya boto3 untuk AWS S3) menggunakan `uv`:

```bash
uv add django-storages boto3
```

---

## Langkah 2: Konfigurasi File Settings Production
Ubah file pengaturan produksi di `config/settings/production.py`:

```python
# config/settings/production.py
import os

INSTALLED_APPS += [
    "storages",
]

# Konfigurasi AWS S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-southeast-3") # Jakarta

# Media files
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# Opsional: Static files ke S3 (jika tidak menggunakan WhiteNoise)
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
```

---

## Langkah 3: Tambahkan Environment Variables
Pastikan Anda mencantumkan variabel lingkungan baru tersebut di file template `.env.example`:

```text
# AWS S3 Storage
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=ap-southeast-3
```

Secara otomatis, semua unggahan berkas (seperti avatar pengguna) sekarang akan dikirimkan langsung ke S3 Bucket.
