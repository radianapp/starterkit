# RDP Starter Kit — Production-Ready Django Template

🚀 **Version 0.1.0** | Production-ready Django starter template untuk Radian Data Platform (RDP).

Developer dapat **clone & jalankan dalam < 5 menit** tanpa setup manual yang berulang.

---

## ✨ Fitur

- ✅ **Custom User Model** — siap extend dengan field custom
- ✅ **Environment Configuration** — semua config dari `.env`, tidak ada hardcode
- ✅ **Security Headers** — production-ready security setup
- ✅ **Admin Panel** — Django admin sudah dikustomisasi
- ✅ **Static & Media Files** — WhiteNoise + local/S3 support
- ✅ **Logging Terstruktur** — development & production-grade logging
- ✅ **Test Suite** — pytest + coverage, siap lanjut development
- ✅ **Cache Backend** — support LocalMemory (dev) & Redis (prod)
- ✅ **Email Backend** — support console/Mailpit (dev) & SMTP (prod)
- ✅ **Django-Cotton Components** — ready untuk UI components

---

## 🚀 Quick Start

### 1. Clone & Setup (5 menit)

```bash
# Clone repository
git clone https://github.com/radianapp/starterkit.git
cd starterkit

# Copy environment template
cp .env.example .env

# Install dependencies (wajib uv, bukan pip)
uv sync --all-groups

# Run migrations
uv run python manage.py migrate

# Create superuser (optional)
uv run python manage.py createsuperuser

# Run development server
uv run python manage.py runserver
```

Buka **http://localhost:8000** — selesai! ✅

### 2. Verify Setup

```bash
# Test suite
uv run pytest

# Linting
uv run ruff check .

# Django system check
uv run python manage.py check --deploy
```

---

## 📁 Project Structure

```
rdp-starter/
├── apps/                    # Django apps (domain-driven)
│   ├── core/                # Utilities, mixins, base views
│   ├── accounts/            # User model, auth (US-003-009)
│   │   ├── models/          # User, UserProfile
│   │   ├── views/
│   │   ├── forms/
│   │   ├── services/        # Business logic
│   │   ├── admin/
│   │   └── migrations/
│   └── dashboard/           # Main page after login (US-001)
├── config/                  # Django configuration
│   ├── settings/
│   │   ├── base.py          # Shared config
│   │   ├── dev.py           # Development overrides
│   │   └── production.py    # Production overrides
│   ├── urls.py              # Root URL config
│   └── wsgi.py
├── templates/               # HTML templates
│   ├── base.html            # Base template (load CDN, blocks)
│   ├── cotton/              # Django-Cotton components
│   ├── dashboard/
│   ├── account/
│   └── errors/              # 403, 404, 500 pages
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploads (local dev)
├── logs/                    # Log files (production)
├── tests/                   # Test suite (pytest)
├── docs/                    # Documentation
│   ├── IMPLEMENTATION-PLAN.md  # 5 phases, 23 user stories
│   ├── PRDv0.1.md
│   └── user-stories/
├── .env.example             # Environment template
├── .env                     # Local development config (gitignore)
├── pyproject.toml           # Dependencies + tool config
├── pytest.ini               # Pytest config (in pyproject.toml)
├── CLAUDE.md                # AI assistant instructions
└── manage.py                # Django CLI
```

---

## ⚙️ Configuration

### Environment Variables

Semua config dari `.env`. Copy `.env.example` dan sesuaikan:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3  # Dev: SQLite
# DATABASE_URL=postgresql://user:password@host:5432/dbname  # Prod

# Cache
CACHE_URL=locmem://  # Dev: Local memory
# CACHE_URL=redis://localhost:6379/0  # Prod

# Email
EMAIL_BACKEND=console  # Dev: Console output
# EMAIL_BACKEND=mailpit  # Mailpit UI testing
# EMAIL_BACKEND=smtp  # Production SMTP
```

Lihat `.env.example` untuk semua variabel & penjelasan.

---

## 🧪 Testing

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_smoke.py -v

# Run with coverage report
uv run pytest --cov=apps --cov-report=html

# Open coverage report
open htmlcov/index.html
```

**Target coverage**: > 80% untuk `apps/`

---

## 📋 Conventions

### Naming
- **App**: lowercase, singular → `accounts`, `dashboard`
- **Model**: PascalCase → `User`, `UserProfile`
- **View**: PascalCase + suffix → `RegisterView`, `DashboardView`
- **URL name**: `{app}:{action}` → `accounts:login`, `dashboard:index`
- **Template**: snake_case → `account/login.html`

### Code
- **Custom User**: `AUTH_USER_MODEL = "accounts.User"` (production-safe)
- **Logging**: Bahasa Indonesia untuk dokumentasi, Bahasa Inggris untuk kode
- **Docstring**: Format wajib dengan TUJUAN, ALUR, DIPANGGIL DARI, DEPENDENSI
- **Services Layer**: Logic bisnis di `services/`, bukan di `views/`

### Struktur Package
Setiap app menggunakan **package per fungsi** (bukan file flat):
```
apps/accounts/
├── models/          # user.py, profile.py
├── views/           # auth.py, profile.py
├── services/        # user_service.py
├── forms/
├── admin/
└── urls.py
```

---

## 📚 Documentation

- **CLAUDE.md** — Project conventions & AI assistant instructions
- **docs/IMPLEMENTATION-PLAN.md** — 5 phases, 23 user stories, Definition of Done
- **docs/user-stories/** — Detailed user stories dengan acceptance criteria
- **docs/PRDv0.1.md** — Product Requirements Document

---

## 🛠️ Development Workflow

### 1. Branch Strategy
```bash
# Feature branch untuk setiap user story
git checkout -b feature/US-004-register

# Commit message format
git commit -m "feat(US-004): Register akun baru

- Tambah RegisterView
- Tambah user_forms.py
- Docs: docs/modules/auth.md"
```

### 2. Before Commit
```bash
# Test
uv run pytest --cov=apps

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Django check
uv run python manage.py check --deploy

# Create migrations if needed
uv run python manage.py makemigrations
```

### 3. Update Docs
- ✅ **CHANGELOG.md** — tambah entry `[Unreleased]`
- ✅ **docs/architecture/database.md** — update ERD jika ada perubahan model
- ✅ **docs/modules/{feature}.md** — dokumentasi modul baru

---

## 🚀 Deployment

### Production Checklist
```bash
# Django check
uv run python manage.py check --deploy

# Collect static files
uv run python manage.py collectstatic --noinput

# Create superuser
uv run python manage.py createsuperuser

# Run migrations
uv run python manage.py migrate

# Start with Gunicorn (bukan runserver)
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Environment Setup (Production)
```bash
# .env untuk production
SECRET_KEY=generate-random-key-di-sini
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://user:password@host:5432/dbname
CACHE_URL=redis://redis-host:6379/0
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password-here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🔗 Dependencies

**Core**:
- Django 4.2+ (LTS)
- Python 3.11+
- uv (package manager)

**Database & Cache**:
- PostgreSQL (production)
- SQLite (development)
- Redis (optional, production cache)

**Dev Tools**:
- pytest + pytest-django
- ruff (linting & formatting)
- django-debug-toolbar

**UI/UX**:
- RDP-UI Design System (CDN: https://cdn.radian.web.id/assets/rdp.css)
- HTMX
- Alpine.js
- django-cotton (components)

---

## 📞 Support

- 📖 Read **CLAUDE.md** untuk project conventions
- 📋 Check **docs/IMPLEMENTATION-PLAN.md** untuk roadmap
- 🤔 See **docs/FAQ.md** untuk common questions

---

## 📝 License

MIT License — see LICENSE file

---

**Buatan**: Radian Data Platform  
**Status**: Version 0.1.0 (Fase 1 Complete: US-001, US-002, US-003)  
**Last Updated**: 2026-06-29
