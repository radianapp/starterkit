# Cookbook: Menambahkan REST API (DRF atau Django Ninja)

Resep ini memandu Anda menambahkan endpoint API RESTful ke dalam RDP Starter Kit menggunakan **Django Ninja** (cepat, asinkron, dan otomatis menghasilkan dokumentasi OpenAPI/Swagger).

---

## Langkah 1: Pasang Django Ninja
Tambahkan library menggunakan `uv`:

```bash
uv add django-ninja
```

---

## Langkah 2: Buat Instance API Global
Buat file `config/api.py` untuk menginisialisasi router API global:

```python
from ninja import NinjaAPI

api = NinjaAPI(
    title="RDP Starter Kit API",
    version="1.0.0",
    description="Dokumentasi interaktif API REST untuk proyek Radian Data Platform"
)
```

Daftarkan router API tersebut di file `config/urls.py`:

```python
from django.urls import path
from .api import api

urlpatterns = [
    # ...
    path("api/v1/", api.urls),
]
```

---

## Langkah 3: Tambahkan Router Endpoint
Buat file `api.py` di dalam aplikasi target Anda (contoh `apps/accounts/api.py`):

```python
from ninja import Router
from django.contrib.auth import get_user_model
from ninja import Schema

router = Router()
User = get_user_model()

class UserOut(Schema):
    id: int
    username: str
    email: str

@router.get("/me", response=UserOut)
def get_current_user(request):
    if not request.user.is_authenticated:
        return 401, {"detail": "Unauthorized"}
    return request.user
```

Daftarkan router accounts ke dalam API global di `config/api.py`:

```python
from config.api import api
from apps.accounts.api import router as accounts_router

api.add_router("/accounts/", accounts_router)
```

---

## Halaman Dokumentasi (OpenAPI)
Jalankan server lokal, lalu buka peramban Anda pada URL:
- **Swagger Docs**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **Redoc**: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
