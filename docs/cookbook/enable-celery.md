# Cookbook: Integrasi Celery untuk Background Tasks

Resep ini menjelaskan cara menambahkan dan mengkonfigurasi Celery di dalam RDP Starter Kit untuk menangani proses asinkronus (seperti pengiriman email masal atau pemrosesan gambar) di latar belakang.

---

## Langkah 1: Pasang Dependencies
Gunakan `uv` untuk menambahkan Celery dan Redis (sebagai message broker):

```bash
uv add celery redis
```

---

## Langkah 2: Buat Instance Celery di Proyek
Buat file `config/celery.py`:

```python
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('rdp_starter')

# Ambil konfigurasi dari settings Django dengan prefix 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task dari seluruh INSTALLED_APPS
app.autodiscover_tasks()
```

Hubungkan Celery di `config/__init__.py` agar dimuat saat Django dijalankan:
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

## Langkah 3: Konfigurasi Broker di Settings
Tambahkan konfigurasi Redis URL pada `config/settings/base.py`:

```python
# Celery Configurations
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

---

## Langkah 4: Tulis Task Pertama
Buat file `tasks.py` di dalam app Anda (misal `apps/accounts/tasks.py`):

```python
from celery import shared_task
import time

@shared_task
def send_marketing_email_task(email_address):
    # Simulasi proses berat
    time.sleep(5)
    print(f"Email berhasil dikirim ke {email_address}")
    return True
```

Panggil task tersebut secara asinkron dari view atau service menggunakan `.delay()`:
```python
send_marketing_email_task.delay("user@example.com")
```
