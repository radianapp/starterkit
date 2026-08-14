# Implementation Plan — RDP Starter Kit v0.2

**Total estimasi**: 59 story points  
**Referensi**: docs/prd/user-stories/rdp-starter-kit.md (dipindah dari docs/user-stories/ — FR-23)  
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
| US-016 | Security headers production-ready | 2 | [x] |
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
- [x] `uv sync` berjalan tanpa error di environment bersih
- [x] `uv run python manage.py migrate` lulus dari database kosong
- [x] `uv run pytest` — 100% pass
- [x] `uv run python manage.py check --deploy` — tidak ada warning kritis
- [x] `AUTH_USER_MODEL = "accounts.User"` terkonfigurasi di `base.py`
- [x] Semua env var terdokumentasi di `.env.example`

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
- [x] `http://localhost:8000` terbuka tanpa error
- [x] RDP-UI CDN ter-load (cek Network tab browser)
- [x] Dark mode mengikuti preferensi OS
- [x] Semua komponen Cotton bisa dirender tanpa error
- [x] URL yang tidak ada menampilkan 404 kustom (bukan Django default)
- [x] `uv run pytest` — masih hijau

---

## Fase 3 — Authentication (15 poin)

> Setelah fase ini, user bisa register, login, logout, reset password, verifikasi email, dan edit profil.

**Prasyarat**: Fase 1 dan Fase 2 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-004 | Register akun baru | 3 | [x] |
| US-005 | Login | 2 | [x] |
| US-006 | Logout | 1 | [x] |
| US-007 | Lupa password & reset | 3 | [x] |
| US-008 | Verifikasi email | 3 | [x] |
| US-009 | Edit profil & avatar | 3 | [x] |

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
- [x] Alur register → verifikasi email → login berjalan end-to-end
- [x] Alur forgot password → email → reset berjalan end-to-end
- [x] Form error tampil sebagai fragment HTMX (response 422, bukan full reload)
- [x] Redirect setelah login menggunakan `HX-Redirect`
- [x] Avatar tersimpan dan tampil di navbar
- [x] `uv run pytest` — masih hijau dengan coverage > 80%

---

## Fase 4 — Authorization & Admin (6 poin)

> Setelah fase ini, permission dan group bisa digunakan di view, dan admin panel sudah rapi.

**Prasyarat**: Fase 3 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-020 | Authorization (Permission & Group) | 3 | [x] |
| US-012 | Admin Django kustom | 3 | [x] |

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
- [x] View dengan `PermissionRequiredMixin` redirect ke 403 untuk user tanpa permission
- [x] Admin panel menampilkan tema kustom (bukan Django default)
- [x] Dark mode berfungsi di admin panel
- [x] `uv run pytest` — masih hijau

---

## Fase 5 — Tooling & Dokumentasi (7 poin)

> Fase terakhir. Setelah ini project benar-benar siap untuk dipakai sebagai starter kit.

**Prasyarat**: Fase 1–4 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-018 | CI/CD GitHub Actions | 3 | [x] |
| US-019 | CLAUDE.md untuk AI assistant | 1 | [x] |
| US-023 | Dokumentasi project | 3 | [x] |

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

## Fase 6 — Layout System & App Shell (8 poin)

> Setelah fase ini, semua 7 layout Cotton tersedia dengan naming v0.2, bebas inline CSS, PicoCSS diload, dan app shell punya persistent theme + toast/modal global.

**Prasyarat**: Fase 1 dan Fase 2 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-027 | Layout system lengkap — 7 komponen Cotton sesuai konvensi v0.2 | 3 | [x] |
| US-026 | Self-host RDP-UI aset via env var | 2 | [x] |
| US-028 | App shell lengkap — persistent theme, toast global, modal global | 3 | [x] |

**Urutan yang disarankan**: US-026 → US-027 → US-028

**File utama yang akan dibuat/diubah**:

```
templates/cotton/layout/
    base.html              # fix: PicoCSS, versioned CDN, skip-nav, debug.css gate
    auth.html              # rename dari blank.html + hapus inline CSS
    public.html            # rename dari home.html + hapus inline CSS
    dashboard.html         # rename dari app.html + toast/modal container
    error.html             # baru
    email.html             # baru — inline CSS safe untuk email client
    print.html             # baru
static/css/
    layout.css             # CSS yang dipindah dari inline
static/js/
    theme.js               # persistent theme via localStorage
    toast.js               # toast global handler
    modal-global.js        # modal global handler
config/settings/base.py    # tambah RDP_UI_VERSION, RDP_UI_SELF_HOST
```

**Checklist selesai Fase 6**:

- [ ] `uv run python manage.py check` — bersih
- [ ] Tidak ada `style="..."` inline di semua file `templates/cotton/layout/`
- [ ] PicoCSS diload sebelum `rdp.css` di semua halaman
- [ ] `debug.css` hanya diload jika `RDP_DEBUG_OVERLAY=True`
- [ ] Theme switcher persist setelah refresh
- [ ] Toast muncul saat server return `HX-Trigger: {"showToast": {...}}`
- [ ] `uv run pytest` — masih hijau

---

## Fase 7 — Component Library (12 poin)

> Setelah fase ini, semua komponen Cotton yang diperlukan tersedia (termasuk komponen gap), halaman demo internal dapat diakses di `/dev/components/`.

**Prasyarat**: Fase 6 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-033 | Komponen Cotton RDP-UI v1.0 gap — badge, avatar, loader | 2 | [x] |
| US-034 | Component library gap — tabs, toast, tooltip, accordion, skeleton, dst. | 8 | [x] |
| US-035 | Halaman demo komponen internal `/dev/components/` | 2 | [x] |

**Urutan yang disarankan**: US-033 → US-034 → US-035

**File utama yang akan dibuat/diubah**:

```
templates/cotton/rdp/
    badge.html
    avatar.html
    loader.html
    tabs.html
    toast.html
    tooltip.html
    accordion.html
    skeleton.html
    empty_state.html
    stat_card.html
    confirm.html           # US-034 + FR-17
    progress.html
    drawer.html
    search_box.html
    filter_bar.html
    file_upload.html
    steps.html
static/css/components/
    badge.css
    avatar.css
    tabs.css
    toast.css
    tooltip.css
    accordion.css
    skeleton.css
    empty-state.css
    stat-card.css
    confirm.css
    progress.css
    drawer.css
    search-box.css
    file-upload.css
    steps.css
apps/core/views/
    dev.py                 # /dev/components/ view (DEBUG only)
config/urls.py             # tambah path dev (if DEBUG)
```

**Checklist selesai Fase 7**:

- [x] Semua komponen bisa dirender tanpa error di `/dev/components/`
- [x] Tidak ada warna hex hardcoded di `static/css/components/*.css` (semua `var(--rdp-*)`)
- [x] `/dev/components/` return 404 saat `DEBUG=False`
- [x] `uv run pytest` — masih hijau

---

## Fase 8 — Public & App Pages + HTMX Patterns (11 poin)

> Setelah fase ini, semua halaman bawaan (public, auth, dashboard, error) siap pakai dan 10 HTMX pattern terimplementasi sebagai contoh hidup.

**Prasyarat**: Fase 6, Fase 7, dan Fase 3 (Auth) selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-029 | HTMX form validation pattern — 422 fragment + HX-Redirect | 2 | [x] |
| US-030 | Layout email + template email transaksional | 2 | [x] |
| US-031 | Public pages — landing, about, terms, privacy | 3 | [x] |
| US-032 | Dashboard default dengan demo data — KPI cards, tabel, pagination | 3 | [x] |
| US-036 | 10 HTMX patterns — contoh hidup + resep cookbook | 5 | [x] |

**Urutan yang disarankan**: US-029 → US-030 → US-031 → US-032 → US-036

**File utama yang akan dibuat/diubah**:

```
apps/core/mixins/
    htmx.py                # HtmxFormMixin — 422 fragment + HX-Redirect
templates/
    email/
        verify_email.html
        password_reset.html
    public/
        landing.html
        about.html
        terms.html
        privacy.html
    dashboard/
        index.html         # update: data dari DB + pagination HTMX
    htmx_examples/
        crud_list.html
        modal_form.html
        delete_confirm.html
        live_validation.html
        inline_edit.html
        search_debounce.html
        pagination_fragment.html
        infinite_scroll.html
        polling.html
        toast_trigger.html
apps/core/views/
    htmx_examples.py       # view untuk setiap HTMX pattern
apps/dashboard/views/
    index.py               # update: query dari DB
config/urls.py             # tambah path public + htmx-examples
```

**Checklist selesai Fase 8**:

- [ ] Landing page tampil di `http://localhost:8000/` tanpa login
- [ ] Dashboard KPI angka dari DB (bukan hardcoded)
- [ ] Semua 10 HTMX pattern accessible dan berfungsi
- [ ] Form error menggunakan HTTP 422 fragment
- [ ] Redirect sukses menggunakan `HX-Redirect`
- [ ] `uv run pytest --cov=apps` — coverage ≥ 80%

---

## Fase 9 — CLI & DX (9 poin)

> Setelah fase ini, developer baru bisa bootstrap project baru dalam < 5 menit via CLI, demo data tersedia, dan lint template berjalan di CI.

**Prasyarat**: Fase 6–8 selesai (layout dan halaman harus final sebelum CLI di-bake).

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-024 | CLI `rdp new` — wizard interaktif bootstrap project | 5 | [x] |
| US-025 | Template app untuk `manage.py startapp --template` | 2 | [x] |
| US-037 | Management command demo data | 2 | [x] |
| US-038 | Script lint template + integrasi CI | 3 | [x] |

**Urutan yang disarankan**: US-037 → US-025 → US-038 → US-024

**File utama yang akan dibuat/diubah**:

```
scripts/
    rdp_new.py             # CLI wizard
    lint_templates.py      # lint inline CSS/JS + hex hardcoded
    app_template/          # template untuk startapp
        models/__init__.py
        views/__init__.py
        services/__init__.py
        forms/__init__.py
        admin/__init__.py
        tests/__init__.py
        urls.py
        apps.py
apps/core/management/commands/
    loaddemodata.py
fixtures/
    demo_data.json
.github/workflows/
    ci.yml                 # update: tambah step "Lint templates"
```

**Checklist selesai Fase 9**:

- [ ] `uv run scripts/rdp_new.py testproject` → `cd testproject && uv sync && uv run python manage.py runserver` dalam < 5 menit
- [ ] `uv run python manage.py loaddemodata` idempotent
- [ ] `uv run python scripts/lint_templates.py` exit 0 di repo yang bersih
- [ ] CI gagal saat ada `style="..."` inline di template
- [ ] `uv run pytest` — masih hijau

---

## Fase 10 — Dokumentasi & SOP (9 poin)

> Fase terakhir v0.2. Setelah ini docs/ terstruktur, semua SOP dan cookbook tersedia, dan skills AI up-to-date.

**Prasyarat**: Fase 1–9 selesai.

| Story | Judul | Estimasi | Status |
|---|---|---|---|
| US-039 | Restrukturisasi `docs/` sesuai standar v0.2 | 2 | [x] |
| US-040 | SOP lengkap — HTMX, Cotton, Git, testing, modul | 3 | [x] |
| US-041 | Cookbook resep langkah-demi-langkah | 3 | [x] |
| US-042 | Workflow update skills AI seiring perubahan konvensi | 1 | [x] |
| US-043 | ERD Analyzer & Generator (`python manage.py generate_erd`) | 2 | [x] |

**Urutan yang disarankan**: US-039 → US-040 → US-041 → US-042 → US-043

**File utama yang akan dibuat/diubah**:

```
docs/
    prd/
        v0.2.md            # sudah ada
        archive/
            PRDv0.1.md     # pindah dari docs/PRDv0.1.md
    prd/user-stories/
        rdp-starter-kit.md # pindah dari docs/user-stories/
    architecture/
        database.md        # diperbarui via generate_erd
    decisions/             # ADR (kosong, siap diisi)
    modules/
        ui-components.md   # sudah ada, update path
        erd-analyzer.md    # spesifikasi modul generate_erd
    sop/
        frontend-structure.md   # pindah dari SOP-FRONTEND-STRUCTURE.md
        htmx-patterns.md        # baru
        cotton-components.md    # baru
        git-workflow.md         # baru
        testing.md              # baru
        module-documentation.md # baru
    cookbook/
        htmx-patterns.md        # baru (dari US-036)
        crud.md                 # baru
        modal-htmx.md           # baru
        wizard.md               # baru
        add-app.md              # baru
        change-app-color.md     # baru
        enable-celery.md        # baru
        enable-asgi.md          # baru
        enable-drf.md           # baru
        enable-s3.md            # baru
        erd-generator.md        # panduan ERD generator
CLAUDE.md                       # update: path docs baru + PRD v0.2
```

**Checklist selesai Fase 10 (= Definition of Done v0.2)**:

- [x] Semua link di CLAUDE.md, README, dan skills menuju path yang benar
- [x] `docs/sop/` berisi ≥ 5 SOP dengan contoh kode konkret
- [x] `docs/cookbook/` berisi ≥ 9 resep (termasuk ERD Generator)
- [x] Semua Acceptance Criteria Fase 5 (v0.1) masih terpenuhi
- [x] `uv run pytest` — 150 passed (100% pass)
- [x] `uv run ruff check .` — bersih (0 error)
- [x] `uv run python manage.py makemigrations --check --dry-run` — bersih (0 pending)
- [x] `uv run python manage.py check --deploy` — bersih (0 error)

---

## Ringkasan Total

| Fase | Stories | Poin | Prasyarat |
|---|---|---|---|
| Fase 1 — Fondasi | US-001,002,003,013,014,016,017,021,022 | 19 | — |
| Fase 2 — UI Shell | US-010,011,015 | 12 | Fase 1 |
| Fase 3 — Auth | US-004,005,006,007,008,009 | 15 | Fase 1, 2 |
| Fase 4 — Authorization & Admin | US-020,012 | 6 | Fase 3 |
| Fase 5 — Tooling & Docs (v0.1) | US-018,019,023 | 7 | Fase 1–4 |
| Fase 6 — Layout System & App Shell | US-026,027,028 | 8 | Fase 1, 2 |
| Fase 7 — Component Library | US-033,034,035 | 12 | Fase 6 |
| Fase 8 — Public & App Pages + HTMX | US-029,030,031,032,036 | 15 | Fase 3, 6, 7 |
| Fase 9 — CLI & DX | US-024,025,037,038 | 12 | Fase 6–8 |
| Fase 10 — Dokumentasi & SOP | US-039,040,041,042 | 9 | Fase 1–9 |
| **Total v0.2** | **42 stories** | **115 poin** | |

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
