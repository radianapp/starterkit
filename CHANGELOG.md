# Changelog

Semua perubahan pada project ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan project ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.2.4] — 2026-07-15

- **Bugfix (Templates)**: Memperbaiki *syntax error* komentar multiline di komponen Cotton (`pagination.html`, `sidebar.html`, `navbar.html`, `breadcrumb.html`) yang menggunakan tag `{#` sehingga muncul ter-render di halaman. Diubah menjadi blok tag `{% comment %}` yang valid.

## [0.2.3] — 2026-07-15

- **Bugfix (UI/UX)**: Menghilangkan duplikasi ikon toolbar (Toggle Dark Mode & Notifikasi) di halaman dashboard.
- **Bugfix (Docs)**: Memperbaiki tautan tombol "Baca Docs" agar mengarah ke repositori dokumentasi Markdown di GitHub, bukan ke rute `/docs/` lokal yang menyebabkan 404.

## [0.2.2] — 2026-07-15

- **Bugfix (Windows)**: Memperbaiki *PermissionError* saat CLI `rdp new` mencoba menghapus folder `.git/` bawaan template (file *pack* bersifat *read-only* di Windows).

## [0.2.1] — 2026-07-15

- **US-024 (CLI Global)**: Refactor `rdp_new.py` menjadi `scripts/rdp_cli.py` — CLI global yang dapat diinstal via `uv tool install` dan dipanggil sebagai `rdp new <nama-proyek>` dari folder mana saja. CLI otomatis meng-*clone* template terbaru dari GitHub, men-*generate* `SECRET_KEY`, menyiapkan `.env`, dan menambahkan halaman opsional.

## [0.2.0] — 2026-07-15

- **RDP UI Framework extras**:
  - Menambahkan sistem tema dinamis (terang/gelap + 9 pilihan aksen warna kustom yang di-persist di localStorage).
  - Menambahkan 3 komponen kustom baru: `<c-rdp.theme_picker>` (widget pemilih tema), `<c-rdp.rating>` (rating bintang interaktif), dan `<c-rdp.timeline>`/`<c-rdp.timeline_item>` (linimasa kronologis vertikal).
  - Membuat utilitas helper HTMX Django (`is_htmx`, `htmx_redirect`, `htmx_refresh`, `htmx_trigger`) untuk efisiensi backend.
  - Membangun halaman landing page promosi dan playground interaktif khusus untuk framework RDP-UI di `/rdp-ui/`.
  - Menulis dokumen PRD khusus dan target metrik kesuksesan untuk RDP-UI Framework di `docs/prd/rdp-ui-framework.md`.
- **US-024**: CLI `rdp new` — Membuat wizard interaktif (`scripts/rdp_new.py`) untuk bootstrap proyek baru dengan opsi kustomisasi warna aksen dan halaman opsional (contact/FAQ).

- **US-025**: Template app untuk `manage.py startapp --template` — Menyediakan template aplikasi kustom (`scripts/app_template`) dengan struktur package (models, views, services, forms, admin, tests) sesuai panduan CLAUDE.md.
- **US-037**: Management command demo data — Menyediakan perintah `python manage.py loaddemodata` secara idempotent untuk menginisialisasi basis data dengan sample user dan data aktivitas dashboard.
- **US-038**: Script lint template + integrasi CI — Membuat skrip validasi statis (`scripts/lint_templates.py`) untuk memastikan kepatuhan SOP frontend (no inline style/script, no hex colors di luar base/tokens) dan mengintegrasikannya pada pipeline CI GitHub Actions.
- **US-029**: HTMX form validation pattern — Membuat `HtmxFormMixin` untuk penanganan form HTMX yang mengembalikan HTTP 422 jika invalid dan `HX-Redirect` header jika sukses.
- **US-030**: Layout email + template email transaksional — Integrasi template email verifikasi dan reset password berbasis `<c-layout.email>` dengan inline-safe CSS.
- **US-031**: Public pages — Implementasi halaman landing page publik, about, terms, dan privacy menggunakan `<c-layout.public>`.
- **US-032**: Dashboard default dengan demo data — Dashboard dinamis terisi data dari database (`Activity` model), dengan tabel terpaginasi HTMX dan placeholder chart SVG premium.
- **US-036**: 10 HTMX patterns — Contoh hidup dari 10 pola HTMX di `/examples/htmx/` dan dokumentasi resep di `docs/cookbook/htmx-patterns.md`.
- **US-033**: Komponen Cotton RDP-UI v1.0 gap — Menambahkan komponen badge, avatar, dan loader dengan props yang terdokumentasi lengkap dan pass-through attributes.
- **US-034**: Component library gap — Menambahkan 14 komponen baru: tabs, toast, tooltip, accordion, skeleton, empty_state, stat_card, confirm, progress, drawer, search_box, filter_bar, file_upload, dan steps dengan styling CSS lokal serta interaktivitas Alpine.js.
- **US-035**: Halaman demo komponen internal `/dev/components/` — Menyediakan halaman dokumentasi dan demo interaktif yang memuat semua komponen beserta contoh kodenya (hanya aktif saat `DEBUG=True`).
- **US-018**: CI/CD GitHub Actions — Setup `.github/workflows/ci.yml` dengan langkah-langkah ruff check, makemigrations check, dan pytest.
- **US-019**: CLAUDE.md — Memverifikasi keselarasan dokumentasi dan instruksi assistant.
- **US-023**: Dokumentasi project — Membuat dokumen `getting-started.md`, `configuration.md`, `cookbook.md`, dan `faq.md` di folder `docs/`.
- **US-012**: Admin Django kustom — jazzmin theme (darkly), search User, icon per model, topmenu links ke app + profil
- **US-020**: Authorization (Permission & Group) — `MultiplePermissionsRequiredMixin`, `RoleRequiredMixin`, `OwnerRequiredMixin` di `apps/core/mixins/`; `@group_required`, `@role_required` di `apps/core/decorators/`; 10 unit tests
- **US-009**: Edit profil & avatar — form edit nama + bio, upload avatar (JPG/PNG/WebP, maks 2MB) via HTMX, preview langsung tanpa reload halaman
- **US-008**: Verifikasi email — token via `django.core.signing` (72 jam), kirim email HTML+TXT setelah register, middleware enforce verifikasi via `REQUIRE_EMAIL_VERIFICATION` env var
- **US-004**: Register akun baru — multi-step wizard via session + HTMX; steps dikonfigurasi dari `REGISTRATION_STEPS` di `.env`; auto-login + redirect dashboard setelah selesai
- **US-005**: Login — form email+password, remember_me (session expire), open-redirect guard, HTMX-aware
- **US-006**: Logout — `POST /accounts/logout/`, clear session, redirect ke login
- **US-007**: Lupa password & reset — Django built-in views, 4 halaman custom, email HTML+TXT
- **US-001**: Clone & jalankan project baru — setup Django, migrations, folder structure
- **US-002**: Konfigurasi environment via `.env` — env var validation, aman untuk git
- **US-003**: Custom User model siap pakai — Custom User extend AbstractUser, UserProfile OneToOne
- **US-010**: Layout dasar (navbar, sidebar, dashboard) — responsive 3-column layout dengan Alpine.js sidebar toggle, dark mode support
- **US-011**: Komponen UI dasar — 9 Cotton components (button, card, alert, modal, table, form.input, form.select, pagination, breadcrumb, dropdown) dengan RDP-UI styling
- **US-015**: Error pages kustom (403, 404, 500) — refactor dengan base.html extension, friendly message, CTA button, responsive design
- **US-017**: Test suite siap pakai — pytest + pytest-django + conftest.py dengan fixtures
- **US-016**: Security headers production-ready — HSTS, CSP, SECURE_SSL_REDIRECT, dll
- **US-021**: Cache (Redis / Local Memory) — support locmem:// & redis://
- **US-022**: Email (SMTP / Console / Mailpit) — support console, mailpit, SMTP backend
- **US-013**: Static & media files — WhiteNoise + django storage
- **SOP & Checklist**: Frontend code organization — SOP-FRONTEND-STRUCTURE.md + FRONTEND-CHECKLIST.md untuk CSS/JS extraction & mobile-first design

### Changed

- **US-010**: Theme system — default light mode; toggle button (🌙/☀️) di navbar + blank layout; preference persist ke `localStorage`; eliminasi `prefers-color-scheme` media query fallback yang konflik
- **base.html**: Refactor dengan clear block structure (navbar_block, sidebar_block, content_block, footer_block), Alpine.js layoutState() untuk sidebar management
- **Error pages**: Extend base.html, add Cotton component styling (card, button), emoji icon, responsive centered layout
- **static/ structure**: Extract CSS (dashboard.css, errors.css) & JS (base.js, layout-state.js) dari inline dalam template — no more inline styles/scripts

### Documentation

- README.md — Quick start, project structure, conventions
- **docs/SOP-FRONTEND-STRUCTURE.md** — Frontend code organization: CSS/JS separation, naming conventions, mobile-first design, workflow
- **docs/FRONTEND-CHECKLIST.md** — Pre-commit checklist untuk template/CSS/JS/komponen validation
- CLAUDE.md — AI assistant instructions (sudah ada, di-verify)
- IMPLEMENTATION-PLAN.md — 5 phases, 23 stories, Definition of Done (sudah ada)
- docs/modules/ui-components.md — Complete component reference dengan examples & best practices
- tests/conftest.py — pytest configuration dengan fixtures

---

## Fase 2 — UI Shell (Completed)

**Status**: Complete (v0.2.0-fase2)  
**Stories**: US-010, US-011, US-015  
**Points**: 12  
**Date**: 2026-06-29

---

## [0.1.0] — 2026-06-29

### Initial Release

- Project skeleton dengan Django, uv, pytest setup
- Custom User model dengan email verification support
- Production-ready security configuration
- Admin panel dengan Custom User inline
- Environment-based configuration (dev/production)
- Test suite dengan 10+ smoke tests
- Documentation & CLAUDE.md untuk AI assistant

**Fase 1 Complete**: US-001, US-002, US-003 ✅

---

Saat release baru, rename `[Unreleased]` → `[vX.Y.Z] — YYYY-MM-DD`
