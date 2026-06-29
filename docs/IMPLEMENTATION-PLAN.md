# Implementation Plan — RDP Starter Kit v0.1

**Total estimasi**: 59 story points  
**Referensi**: docs/prd/user-stories/rdp-starter-kit.md  
**Dibuat**: 2026-06-29

---

## Cara Baca Dokumen Ini

Sebelum mulai koding setiap fase:
1. Baca semua user stories di fase tersebut
2. Pastikan semua story di fase sebelumnya sudah **Done**
3. Tandai story sebagai `[x]` saat selesai
4. Jalankan `uv run pytest` — wajib hijau sebelum pindah fase

---

## Fase 1 — Fondasi (19 poin)

> Tidak ada halaman yang tampil dulu. Ini "tulang" project — semua konfigurasi, model, dan tooling dasar.

**Prasyarat**: Tidak ada. Ini fase pertama.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-001 | Clone & jalankan project baru | 2 | [x] |
| US-002 | Konfigurasi environment via `.env` | 2 | [x] |
| US-003 | Custom User model siap pakai | 2 | [x] |
| US-016 | Security headers production-ready | 2 | [ ] |
| US-021 | Cache (Redis / Local Memory) | 2 | [x] |
| US-022 | Email (SMTP / Console / Mailpit) | 2 | [x] |
| US-013 | Static & media files | 2 | [x] |
| US-014 | Logging terstruktur | 2 | [x] |
| US-017 | Test suite siap pakai | 3 | [x] |

**Urutan yang disarankan**: US-001 → US-002 → US-003 → US-016 → US-021 → US-022 → US-013 → US-014 → US-017

**File utama yang akan dibuat/diubah**:
```
pyproject.toml
.env.example
manage.py
config/settings/base.py
config/settings/dev.py
config/settings/production.py
config/urls.py
config/wsgi.py
apps/core/__init__.py
apps/accounts/models/            # US-003: package, bukan flat file
    __init__.py                  # import User, Profile
    user.py                      # US-003: Custom User (AbstractUser)
    profile.py                   # US-003: UserProfile (OneToOne)
apps/accounts/migrations/
logs/                            # US-014
tests/conftest.py                # US-017
pytest.ini (atau pyproject.toml) # US-017
```

**Checklist selesai Fase 1**:
- [ ] `uv sync` berjalan tanpa error di environment bersih
- [ ] `uv run python manage.py migrate` lulus dari database kosong
- [ ] `uv run pytest` — 100% pass
- [ ] `uv run python manage.py check --deploy` — tidak ada warning kritis
- [ ] `AUTH_USER_MODEL = "accounts.User"` terkonfigurasi di `base.py`
- [ ] Semua env var terdokumentasi di `.env.example`

---

## Fase 2 — UI Shell (12 poin)

> Setelah fase ini, developer bisa membuka browser dan melihat halaman. Masih belum ada fitur, tapi layout dan komponen sudah tersedia.

**Prasyarat**: Fase 1 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-010 | Layout dasar (navbar, sidebar, dashboard) | 5 | [x] |
| US-011 | Komponen UI dasar | 5 | [x] |
| US-015 | Error pages kustom (403, 404, 500) | 2 | [x] |

**Urutan yang disarankan**: US-010 → US-011 → US-015

**File utama yang akan dibuat/diubah**:
```
templates/base.html              # US-010: load RDP-UI CDN, HTMX, Alpine.js
templates/cotton/rdp/
    layout/navbar.html           # US-010
    layout/sidebar.html          # US-010
    layout/dashboard.html        # US-010
    button.html                  # US-011
    card.html                    # US-011
    alert.html                   # US-011
    modal.html                   # US-011
    table.html                   # US-011
    form/input.html              # US-011
    form/select.html             # US-011
    pagination.html              # US-011
    breadcrumb.html              # US-011
    dropdown.html                # US-011
templates/errors/
    403.html                     # US-015
    404.html                     # US-015
    500.html                     # US-015
config/urls.py                   # US-015: daftarkan handler403/404/500
apps/dashboard/views.py          # halaman index setelah login
apps/dashboard/urls.py
```

**Checklist selesai Fase 2**:
- [ ] `http://localhost:8000` terbuka tanpa error
- [ ] RDP-UI CDN ter-load (cek Network tab browser)
- [ ] Dark mode mengikuti preferensi OS
- [ ] Semua komponen Cotton bisa dirender tanpa error
- [ ] URL yang tidak ada menampilkan 404 kustom (bukan Django default)
- [ ] `uv run pytest` — masih hijau

---

## Fase 3 — Authentication (15 poin)

> Setelah fase ini, user bisa register, login, logout, reset password, verifikasi email, dan edit profil.

**Prasyarat**: Fase 1 dan Fase 2 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-004 | Register akun baru | 3 | [ ] |
| US-005 | Login | 2 | [ ] |
| US-006 | Logout | 1 | [ ] |
| US-007 | Lupa password & reset | 3 | [ ] |
| US-008 | Verifikasi email | 3 | [ ] |
| US-009 | Edit profil & avatar | 3 | [ ] |

**Urutan yang disarankan**: US-004 → US-005 → US-006 → US-007 → US-008 → US-009

**File utama yang akan dibuat/diubah**:
```
apps/accounts/
    views/                      # package
        __init__.py
        auth.py                 # US-004,005,006,007,008: RegisterView, LoginView, LogoutView, dll.
        profile.py              # US-009: ProfileView, AvatarUpdateView
    forms/                      # package
        __init__.py
        user_forms.py           # US-004,005,007,009: RegisterForm, LoginForm, ProfileForm, dll.
    services/                   # package — logic bisnis bukan di views
        __init__.py
        user_service.py         # US-008: send_verification_email(), US-009: resize_avatar()
    models/
        profile.py              # US-009: tambah avatar field ke UserProfile
    migrations/
    urls.py
templates/account/
    login.html                  # US-005
    register.html               # US-004
    forgot_password.html        # US-007
    password_reset_confirm.html # US-007
    email_verification.html     # US-008
    profile.html                # US-009
templates/cotton/rdp/
    users/login-form.html       # komponen form login
    users/register-form.html
    users/profile-form.html
```

**Checklist selesai Fase 3**:
- [ ] Alur register → verifikasi email → login berjalan end-to-end
- [ ] Alur forgot password → email → reset berjalan end-to-end
- [ ] Form error tampil sebagai fragment HTMX (response 422, bukan full reload)
- [ ] Redirect setelah login menggunakan `HX-Redirect`
- [ ] Avatar tersimpan dan tampil di navbar
- [ ] `uv run pytest` — masih hijau dengan coverage > 80%

---

## Fase 4 — Authorization & Admin (6 poin)

> Setelah fase ini, permission dan group bisa digunakan di view, dan admin panel sudah rapi.

**Prasyarat**: Fase 3 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-020 | Authorization (Permission & Group) | 3 | [ ] |
| US-012 | Admin Django kustom | 3 | [ ] |

**Urutan yang disarankan**: US-020 → US-012

**File utama yang akan dibuat/diubah**:
```
apps/core/
    mixins/                      # package
        __init__.py
        auth_mixins.py           # US-020: PermissionRequiredMixin kustom
    decorators/                  # package
        __init__.py
        auth_decorators.py       # US-020: contoh @permission_required
apps/accounts/
    admin/                       # package
        __init__.py
        user_admin.py            # US-012: User + UserProfile admin kustom
config/settings/base.py          # US-012: admin theme config
templates/admin/                 # US-012: override template admin
```

**Checklist selesai Fase 4**:
- [ ] View dengan `PermissionRequiredMixin` redirect ke 403 untuk user tanpa permission
- [ ] Admin panel menampilkan tema kustom (bukan Django default)
- [ ] Dark mode berfungsi di admin panel
- [ ] `uv run pytest` — masih hijau

---

## Fase 5 — Tooling & Dokumentasi (7 poin)

> Fase terakhir. Setelah ini project benar-benar siap untuk dipakai sebagai starter kit.

**Prasyarat**: Fase 1–4 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-018 | CI/CD GitHub Actions | 3 | [ ] |
| US-019 | CLAUDE.md untuk AI assistant | 1 | [ ] |
| US-023 | Dokumentasi project | 3 | [ ] |

**Urutan yang disarankan**: US-018 → US-019 → US-023

**File utama yang akan dibuat/diubah**:
```
.github/workflows/
    ci.yml                       # US-018: lint → test → migration check
CLAUDE.md                        # US-019: sudah ada, update jika perlu
docs/
    getting-started.md           # US-023: sudah ada
    configuration.md             # US-023: sudah ada
    cookbook.md                  # US-023: sudah ada
    faq.md                       # US-023: sudah ada
```

**Checklist selesai Fase 5 (= Definition of Done seluruh project)**:
- [ ] Push ke GitHub → GitHub Actions hijau (lint + test + migration check)
- [ ] `uv run pytest --cov=apps` — coverage > 80%
- [ ] `uv run python manage.py check --deploy` — bersih
- [ ] `uv run python manage.py makemigrations --check --dry-run` — tidak ada migration ketinggalan
- [ ] Install ulang dari `uv sync` di virtual environment bersih — tidak ada dependency yang missing
- [ ] Clone fresh + ikuti `docs/getting-started.md` → runserver dalam < 5 menit
- [ ] `CLAUDE.md` akurat dengan kode yang ada

---

## Ringkasan Total

| Fase | Stories | Poin | Prasyarat |
|---|---|---|---|
| Fase 1 — Fondasi | US-001,002,003,013,014,016,017,021,022 | 19 | — |
| Fase 2 — UI Shell | US-010,011,015 | 12 | Fase 1 |
| Fase 3 — Auth | US-004,005,006,007,008,009 | 15 | Fase 1, 2 |
| Fase 4 — Authorization & Admin | US-020,012 | 6 | Fase 3 |
| Fase 5 — Tooling & Docs | US-018,019,023 | 7 | Fase 1–4 |
| **Total** | **23 stories** | **59 poin** | |

---

## Definition of Done — Per Story

Checklist ini wajib dipenuhi sebelum story ditandai `[x]` dan pindah ke story berikutnya.

### Kode
- [ ] Semua acceptance criteria dari user story terpenuhi
- [ ] Setiap file Python yang dibuat/diubah memiliki referensi US di docstring/komentar (`US: US-{nomor} — {judul}`)
- [ ] Setiap template HTML yang dibuat/diubah memiliki referensi US (`{# US-{nomor}: {judul} #}`)

### Test
- [ ] `uv run pytest` — 100% pass
- [ ] Coverage tidak turun di bawah 80% (`uv run pytest --cov=apps`)

### Kualitas
- [ ] `uv run ruff check .` — bersih tanpa warning
- [ ] `uv run python manage.py makemigrations --check --dry-run` — tidak ada migration ketinggalan

### Dokumentasi
- [ ] `CHANGELOG.md` diupdate — tambah entri di `[Unreleased]` dengan format `US-{nomor}: {judul} — {deskripsi singkat}`
- [ ] Jika `models.py` diubah → `docs/architecture/database.md` (ERD) diupdate
- [ ] Jika fitur cukup kompleks → `docs/modules/{nama}.md` dibuat/diupdate

### Commit
```bash
git add .
git commit -m "feat(US-{nomor}): {deskripsi singkat}

- {detail perubahan 1}
- {detail perubahan 2}
US: US-{nomor} — {judul story}"
```

---

## Perintah Wajib Per Story

```bash
# Jalankan ketiganya sebelum commit
uv run pytest --cov=apps
uv run python manage.py makemigrations --check --dry-run
uv run ruff check .
```

Jika salah satu gagal → story belum Done, jangan pindah ke story berikutnya.
