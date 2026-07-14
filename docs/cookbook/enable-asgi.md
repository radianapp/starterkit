# Cookbook: Konfigurasi ASGI dan WebSockets

Resep ini menjelaskan langkah-langkah beralih dari mode WSGI (sinkronus) ke ASGI (asinkronus) menggunakan **Django Channels** untuk mendukung fitur real-time seperti WebSockets.

---

## Langkah 1: Pasang Channels
Tambahkan library Channels dan daphne (web server ASGI) menggunakan `uv`:

```bash
uv add channels daphne
```

---

## Langkah 2: Daftarkan App Channels
Daftarkan `daphne` di urutan paling atas dari `INSTALLED_APPS` pada file `config/settings/base.py`:

```python
INSTALLED_APPS = [
    "daphne",  # Wajib ditaruh paling atas sebelum django.contrib.staticfiles
    # ...
    "django.contrib.staticfiles",
    "channels",
    # ...
]
```

Definisikan routing ASGI application:
```python
# config/settings/base.py
ASGI_APPLICATION = "config.asgi.application"
```

---

## Langkah 3: Konfigurasi File ASGI
Ubah file `config/asgi.py` agar menangani protokol HTTP dan WebSocket:

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# Inisialisasi HTTP ASGI handler awal
django_asgi_app = get_asgi_application()

import apps.core.routing # Taruh routing WebSocket aplikasi di sini

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.core.routing.websocket_urlpatterns
        )
    ),
})
```

---

## Langkah 4: Jalankan Server ASGI
Saat development, server runserver akan otomatis mendeteksi konfigurasi ASGI dan menggunakan daphne.

Untuk production, jalankan menggunakan command daphne:
```bash
uv run daphne -b 0.0.0.0 -p 8000 config.asgi:application
```
