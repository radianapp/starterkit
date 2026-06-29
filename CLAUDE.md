# RDP Starter Kit — Context untuk AI Assistant

## Apa ini?

Template project Django production-ready untuk semua produk Radian Data Platform (RDP). Tujuan: developer bisa clone dan langsung fokus ke fitur bisnis dalam < 5 menit.

---

## Tech Stack

| Layer | Pilihan |
|---|---|
| Framework | Django (latest stable) |
| Package manager | `uv` — **wajib**, jangan pakai pip langsung |
| Database | PostgreSQL (prod) / SQLite (dev/test) |
| CSS | PicoCSS + RDP-UI (`cdn.radian.web.id`) |
| Component | django-cotton (`<c-rdp.{nama}>`) |
| Interaktivitas | HTMX + Alpine.js |
| Static files | WhiteNoise |
| WSGI | Gunicorn |
| Linting + format | Ruff |
| Testing | Pytest + pytest-cov |

---

## Struktur Folder

```
rdp-starter/
├── apps/
│   ├── core/                   ← context processors, mixins, base views, utils
│   ├── accounts/               ← Custom User model, auth views (login/register/profile)
│   │   ├── models/             ← package: user.py, profile.py (bukan models.py flat)
│   │   │   ├── __init__.py     ← import semua model publik di sini
│   │   │   ├── user.py
│   │   │   └── profile.py
│   │   ├── views/              ← package: auth.py, profile.py
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── profile.py
│   │   ├── services/           ← logic bisnis: user_service.py, email_service.py
│   │   │   ├── __init__.py
│   │   │   └── user_service.py
│   │   ├── forms/
│   │   │   ├── __init__.py
│   │   │   └── user_forms.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   └── user_admin.py
│   │   └── urls.py
│   └── dashboard/              ← halaman utama setelah login
│
├── config/
│   ├── settings/
│   │   ├── base.py     ← settings utama, INSTALLED_APPS, AUTH_USER_MODEL
│   │   ├── dev.py      ← override untuk development (DEBUG=True, SQLite, email console)
│   │   └── production.py ← override untuk production (security headers, S3, SMTP)
│   ├── urls.py         ← root URL conf + handler 403/404/500
│   └── wsgi.py
│
├── templates/
│   ├── cotton/         ← komponen django-cotton yang bisa di-override per project
│   │   └── rdp/        ← namespace komponen: <c-rdp.button>, <c-rdp.card>, dst.
│   ├── base.html       ← load RDP-UI CDN + HTMX + Alpine.js, extend ini
│   ├── account/        ← login, register, forgot password, profile
│   └── errors/         ← 403.html, 404.html, 500.html
│
├── static/             ← static files project (override CDN jika perlu)
├── media/              ← upload files (local dev)
├── logs/               ← log files (production)
├── tests/              ← test files, ikuti struktur apps/
├── docs/               ← semua dokumentasi project
│   ├── prd/            ← Product Requirements Document
│   ├── architecture/   ← Architecture Design + ERD (database.md wajib update saat models/ berubah)
│   ├── decisions/      ← Architecture Decision Records (ADR)
│   └── prd/user-stories/ ← User Stories
│
├── .github/workflows/  ← CI: lint → test → migration check
├── .env.example        ← template semua env var (salin ke .env)
├── pyproject.toml      ← dependency + tool config (ruff, pytest)
├── CLAUDE.md           ← file ini
└── manage.py
```

> **Penting**: Semua app Django menggunakan **package per fungsi** — bukan file flat. `models/`, `views/`, `services/`, `forms/`, `admin/` masing-masing adalah folder dengan `__init__.py`. Logic bisnis wajib di `services/`, bukan di `views/`.

---

## Konvensi Wajib

**Referensi User Story di Kode**

Setiap file, class, atau function yang mengimplementasikan user story **wajib** mencantumkan referensi US-nya sebagai komentar/docstring. Ini memudahkan tracing antara kode dan requirement.

```python
# apps/accounts/views.py

class RegisterView(FormView):
    """
    Handle registrasi akun baru.
    US: US-004 — Register akun baru
    Ref: docs/prd/user-stories/rdp-starter-kit.md
    """

def send_verification_email(user):
    """
    Kirim email verifikasi ke user baru.
    US: US-008 — Verifikasi email
    """
```

```python
# apps/accounts/models.py
# US-003: Custom User model siap pakai

class User(AbstractUser):
    ...
```

```html
{# templates/account/login.html #}
{# US-005: Login #}
{% extends "base.html" %}
```

Format: `US: US-{nomor} — {judul story}` — singkat, di baris pertama docstring atau sebagai komentar di atas class/function.

---

**Naming**
- App Django: lowercase, singular, tanpa tanda hubung → `accounts`, `dashboard`, `billing`
- Model: PascalCase, singular → `UserProfile`, `AuditLog`
- View: PascalCase + suffix tipe → `DashboardView`, `UserLoginView`
- URL name: `{app}:{action}` → `accounts:login`, `dashboard:index`
- Template: snake_case, di folder app → `templates/accounts/login.html`
- Cotton component: `templates/cotton/rdp/{nama}.html` → dipanggil `<c-rdp.{nama}>`

**Settings**
- `AUTH_USER_MODEL = "accounts.User"` — **jangan pernah diubah setelah migrate pertama**
- Semua nilai sensitif dari env, tidak ada hardcode di settings
- `DJANGO_SETTINGS_MODULE` di-set via `.env` atau environment

**HTMX**
- Response partial (fragment): kembalikan hanya fragment HTML yang relevan
- Response error form: gunakan HTTP 422 (bukan 200) agar HTMX tahu ini error
- Full page redirect setelah sukses: gunakan header `HX-Redirect`

**django-cotton**
- Komponen bawaan starter: namespace `<c-rdp.{nama}>` (misal `<c-rdp.button>`)
- Override komponen: buat file di `templates/cotton/rdp/{nama}.html` di project ini
- Jangan pakai utility CSS bebas di template — styling lewat komponen atau CSS var RDP-UI

**Test**
- Setiap view/model baru wajib ada test-nya di `tests/`
- Jalankan `uv run pytest` sebelum commit — wajib hijau
- Coverage target: > 80% untuk kode di `apps/`

---

## Cara Jalankan

```bash
# Setup awal (sekali)
cp .env.example .env
uv sync

# Migrasi & superuser
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Development server
uv run python manage.py runserver

# Test
uv run pytest
uv run pytest --cov=apps -v

# Lint & format
uv run ruff check .
uv run ruff format .

# Buat migrasi setelah ubah model
uv run python manage.py makemigrations
uv run python manage.py migrate

# Shell Django
uv run python manage.py shell
```

---

## Wajib Setelah Setiap Story Selesai

### 1. Update CHANGELOG.md
Setiap story yang selesai (`[x]` di IMPLEMENTATION-PLAN.md) **wajib** ditambahkan ke bagian `[Unreleased]` di `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- US-004: Register akun baru — form register + email verifikasi
- US-005: Login — form login + redirect ke dashboard

### Changed
- US-009: Profil — tambah field avatar
```

Format entri: `US-{nomor}: {judul} — {deskripsi singkat apa yang berubah}`

Saat rilis versi baru: rename `[Unreleased]` → `[vX.Y.Z] — YYYY-MM-DD`.

### 2. Update ERD jika ada perubahan model
Setiap kali file di `models/` diubah (tambah model, tambah field, ubah relasi), **wajib** update `docs/architecture/database.md`:

- Tambah model baru → tambah entity baru di diagram Mermaid
- Tambah field baru → update entity yang relevan
- Tambah relasi (FK, M2M, OneToOne) → tambah garis relasi
- Hapus field/model → hapus dari diagram

ERD **tidak** perlu diupdate jika perubahan hanya di view, form, service, template, atau serializer.

---

## Rencana Implementasi

Lihat `docs/IMPLEMENTATION-PLAN.md` untuk:
- Urutan fase pengerjaan (5 fase)
- Story mana yang masuk fase mana
- Checklist selesai per fase
- File-file yang akan dibuat per fase

---

## File Penting yang Perlu Diketahui

| File | Isi |
|---|---|
| `config/settings/base.py` | `INSTALLED_APPS`, `AUTH_USER_MODEL`, middleware, template, cache, email |
| `config/settings/dev.py` | SQLite, email console, DEBUG=True |
| `config/settings/production.py` | PostgreSQL, SMTP, security headers, WhiteNoise |
| `config/urls.py` | Root URL conf, daftarkan `handler403/404/500` di sini |
| `apps/accounts/models/user.py` | Custom User model — extend `AbstractUser` |
| `apps/accounts/models/__init__.py` | Import semua model publik (wajib untuk backward compat) |
| `apps/accounts/services/user_service.py` | Logic bisnis: send email, update profil, dll. |
| `templates/base.html` | Base template — load CDN, block content/scripts |
| `.env.example` | Semua env var yang tersedia |
| `docs/configuration.md` | Penjelasan detail setiap env var |
| `docs/cookbook.md` | Cara aktifkan fitur opsional (Celery, ASGI, S3, DRF) |
| `docs/IMPLEMENTATION-PLAN.md` | 5 fase implementasi, urutan story, checklist per fase |
| `docs/prd/user-stories/rdp-starter-kit.md` | 23 user stories dengan acceptance criteria |

---

## Hal yang TIDAK Boleh Dilakukan

- Jangan ubah `AUTH_USER_MODEL` setelah ada data di database
- Jangan hardcode `SECRET_KEY`, password, atau API key di kode
- Jangan `pip install` — selalu `uv add`
- Jangan taruh logic bisnis di `config/` — itu hanya untuk konfigurasi
- Jangan commit file `.env` — hanya `.env.example`
- Jangan pakai `*` sebagai versi dependency di `pyproject.toml`
