# Cookbook: Menambah Django App Baru

Resep ini menjelaskan langkah-langkah menambahkan modul atau Django application baru ke dalam proyek RDP Starter Kit dengan struktur folder yang terorganisir.

---

## Langkah 1: Buat Struktur Aplikasi Baru
RDP Starter Kit tidak menggunakan file flat (`models.py`, `views.py`). Jalankan boilerplate template generator untuk membuat modul:

```bash
uv run python manage.py startapp <nama_app> --template=scripts/app_template
```

Jika generator tidak tersedia, buat struktur berikut secara manual:
```text
apps/<nama_app>/
├── __init__.py
├── apps.py
├── admin/
│   ├── __init__.py
│   └── <nama_app>_admin.py
├── forms/
│   ├── __init__.py
│   └── <nama_app>_forms.py
├── models/
│   ├── __init__.py
│   └── <nama_app>_models.py
├── services/
│   ├── __init__.py
│   └── <nama_app>_service.py
├── views/
│   ├── __init__.py
│   └── <nama_app>_views.py
├── urls.py
└── tests/
    ├── __init__.py
    └── test_views.py
```

---

## Langkah 2: Daftarkan App Baru di Settings
Tambahkan nama aplikasi baru ke dalam list `INSTALLED_APPS` di `config/settings/base.py`:

```python
# config/settings/base.py
INSTALLED_APPS = [
    # ...
    "apps.core",
    "apps.accounts",
    "apps.<nama_app>",  # Daftarkan di sini
]
```

---

## Langkah 3: Konfigurasi Routing URL
1. Tulis router url lokal di `apps/<nama_app>/urls.py`:
   ```python
   from django.urls import path
   from apps.<nama_app>.views import IndexView

   app_name = "<nama_app>"
   urlpatterns = [
       path("", IndexView.as_view(), name="index"),
   ]
   ```

2. Daftarkan router tersebut ke root URL conf di `config/urls.py`:
   ```python
   urlpatterns = [
       # ...
       path("<nama_app>/", include("apps.<nama_app>.urls", namespace="<nama_app>")),
   ]
   ```
