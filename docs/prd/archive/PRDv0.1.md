# PRD: RDP Starter Kit

| Field | Value |
|---|---|
| Versi | v0.1 |
| Status | Review |
| Tanggal | 2026-06-29 |
| Owner | KK |

## 1. Background & Problem

KK mengelola 10+ produk SaaS sebagai solo founder. Setiap project baru dimulai dari nol: setup auth, halaman statis, konfigurasi env, CI, security header, struktur folder — semua ditulis ulang dengan cara yang berbeda-beda per project. Hasilnya:

- Waktu setup project baru memakan 1–2 hari, padahal kode-nya hampir identik antar project.
- Tidak ada standar baku — setiap project drift dalam hal struktur folder, naming convention, dan cara pakai HTMX + django-cotton + RDP-UI.
- Bug yang sama muncul berulang karena fix tidak tersebar ke project lain.
- Developer baru (atau AI assistant) butuh waktu lebih lama untuk orientasi karena setiap project berbeda.

---

## 2. Goals

- Setup project baru dari nol sampai `runserver` selesai dalam **< 5 menit**.
- Semua project RDP memiliki struktur, naming, dan konfigurasi yang konsisten.
- Project yang di-generate langsung production-ready: security, logging, CI sudah terkonfigurasi.
- AI assistant (Claude, dll.) dapat memahami struktur project tanpa penjelasan tambahan.

## Non-Goals

- Bukan pengganti dokumentasi bisnis per produk (Taliti, Akun, Bayar, dll.) — starter kit hanya fondasi teknis.
- Tidak menyediakan fitur billing, notifikasi, atau audit log out-of-the-box di v0.1 — fitur ini ditambahkan manual per project sesuai kebutuhan.
- Tidak mendukung multi-tenant di v0.1.
- Tidak ada private PyPI / package registry — distribusi cukup via git clone.
- Tidak ada CLI generator interaktif di v0.1 — generate project cukup dengan `git clone` + hapus manual fitur yang tidak diperlukan (atau via script sederhana).

---

## 3. Success Metric

- **Setup time**: Developer baru bisa menjalankan `runserver` dalam < 5 menit dari clone (diukur dari stopwatch saat onboarding project baru pertama kali).
- **Test pass rate**: 100% test lulus segera setelah `uv run pytest` di project yang baru di-generate, tanpa konfigurasi tambahan.
- **CI green on day 1**: GitHub Actions hijau sejak commit pertama di project baru yang menggunakan starter kit ini.
- **Adoption**: Minimal 3 project RDP aktif (dari 10+ yang ada) berjalan di atas starter kit ini dalam 60 hari setelah v0.1 rilis.

---

## 4. User Persona

**KK — Solo Founder / Lead Developer RDP**
Mengelola 10+ produk SaaS sendirian. Butuh fondasi yang "sudah beres" supaya bisa langsung fokus ke fitur bisnis, bukan setup infrastruktur. Terbiasa dengan Django, PostgreSQL, HTMX, uv. Menggunakan AI assistant (Claude) secara intensif — struktur project yang konsisten dan AI-friendly adalah kebutuhan nyata, bukan nice-to-have.

---

## 5. Scope

### In Scope

- Template project Django siap clone + jalankan.
- Custom User model sudah dikonfigurasi.
- Auth lengkap: login, logout, register, forgot password, email verification, profile, avatar.
- Authorization: permission, group, role berbasis Django built-in.
- UI dasar: layout (navbar, sidebar, dashboard, settings), komponen (button, modal, alert, card, table, form, pagination, breadcrumb, dropdown) menggunakan PicoCSS + RDP-UI + django-cotton.
- Admin Django yang dikustomisasi (dashboard, search, filter, dark mode).
- Konfigurasi via `.env` (DEBUG, SECRET_KEY, DATABASE, EMAIL, STORAGE, CACHE).
- Logging terstruktur (output ke console + file).
- Error pages custom (403, 404, 500).
- Static & media support (local dan S3-compatible).
- Cache support (Redis atau local memory) — dikonfigurasi via env.
- Email support (SMTP, console, Mailpit untuk development) — dikonfigurasi via env.
- Security siap produksi: HTTPS, secure cookie, CSP, CSRF, HSTS.
- Quality tooling: Ruff (format + lint), Pytest + pytest-cov, pre-commit.
- CI/CD: GitHub Actions (lint → test → migration check).
- Struktur folder standar yang konsisten dan AI-friendly.
- `CLAUDE.md` di root project berisi ringkasan struktur dan konvensi untuk AI assistant.
- Dokumentasi: Getting Started, Architecture, Configuration, FAQ, Cookbook.

### Out of Scope

- Background task (Celery) — instruksi di docs, tidak dikonfigurasi by default.
- WebSocket (Django Channels) — instruksi di docs.
- ASGI — instruksi di docs cara mengaktifkan, default WSGI (Gunicorn).
- REST API (DRF + JWT + Swagger) — instruksi di docs.
- GraphQL (Strawberry) — instruksi di docs.
- Full-text search (PostgreSQL tsvector / Meilisearch) — instruksi di docs.
- Monitoring (Sentry, Prometheus) — instruksi di docs.
- Docker — instruksi di docs, tidak disertakan sebagai file template.
- CLI generator interaktif (`rdp new myproject`) — roadmap v0.2.
- Deployment template (VPS, Railway, Fly.io, Render) — roadmap v0.2.

---

## 6. Functional Requirements

**FR-01** — Developer dapat clone repo starter kit dan menjalankan `uv run python manage.py runserver` tanpa langkah konfigurasi tambahan selain menyalin `.env.example` ke `.env`.

**FR-02** — Project yang di-generate menyertakan Custom User model yang sudah aktif (`AUTH_USER_MODEL` sudah di-set di `settings/base.py`). Tidak ada migrasi yang berbenturan jika developer langsung menjalankan `migrate`.

**FR-03** — Alur auth lengkap (register, login, logout, forgot password, email verification) berfungsi out-of-the-box menggunakan komponen django-cotton + RDP-UI tanpa konfigurasi tambahan.

**FR-04** — Layout dasar (navbar, sidebar, dashboard, settings) tersedia sebagai template Cotton yang bisa di-override per project.

**FR-05** — Konfigurasi environment terpusat di `.env`. Semua nilai sensitif (SECRET_KEY, DATABASE_URL, dll.) tidak boleh hardcoded di settings.

**FR-06** — `uv run pytest` lulus 100% segera setelah clone tanpa konfigurasi tambahan.

**FR-07** — GitHub Actions berjalan otomatis pada setiap push: lint (Ruff), test (Pytest), migration check, dan build Docker (jika Dockerfile ada).

**FR-08** — Admin Django sudah dikustomisasi: tampilan dashboard, search, filter, tema, dan dark mode aktif by default.

**FR-09** — Static files dilayani via WhiteNoise (development dan production). Konfigurasi S3 tersedia via env var tanpa mengubah kode.

**FR-10** — Logging terstruktur aktif by default: output ke console (development) dan file (production). Format JSON untuk production.

**FR-11** — Error pages custom (403, 404, 500) sudah terdaftar dan menggunakan layout yang konsisten dengan UI project.

**FR-12** — `CLAUDE.md` di root berisi: deskripsi singkat project, struktur folder, konvensi naming, tech stack yang dipakai, dan cara menjalankan dev server + test.

**FR-13** — Authorization berbasis Django built-in (Permission, Group) sudah terkonfigurasi. Tersedia mixin/decorator untuk cek permission di view, dan contoh penggunaan di kode.

**FR-14** — Cache dikonfigurasi via env (`CACHE_URL`): Redis untuk production, local memory untuk development. Swap backend tidak membutuhkan perubahan kode.

**FR-15** — Email dikonfigurasi via env (`EMAIL_BACKEND`): console untuk development, Mailpit untuk testing email HTML, SMTP untuk production.

**FR-16** — Dokumentasi tersedia di folder `docs/`: Getting Started, Configuration reference, Architecture, FAQ, dan Cookbook (contoh resep umum seperti cara tambah app baru, cara aktifkan Celery, cara aktifkan ASGI).

---

## 7. Non-Functional Requirements

**Performa:** `uv run python manage.py runserver` boot dalam < 5 detik di mesin development standar. `uv sync` (install dependency) selesai dalam < 2 menit dari koneksi internet normal.

**Keamanan:** Konfigurasi default production-safe — `DEBUG=False` di `settings/production.py`, `ALLOWED_HOSTS` wajib diisi via env, CSRF aktif, secure cookie aktif, CSP header terpasang via middleware.

**Maintainability:** Struktur folder konsisten di semua project yang menggunakan starter kit. Naming convention didokumentasikan di `CLAUDE.md`. Tidak ada "magic" yang tidak terdokumentasi.

**AI Friendliness:** Folder dan file diberi nama yang deskriptif. Komentar secukupnya di kode yang tidak self-explanatory. Struktur flat lebih diutamakan daripada nested yang dalam.

**Dependency:** Minimal — tidak ada package yang dipasang tanpa alasan jelas. Setiap dependency wajib ada di `pyproject.toml` dengan range versi yang jelas (bukan `*`).

**Coverage:** Minimal 80% coverage untuk kode di `apps/` yang di-generate.

---

## 8. Dependencies

- Python latest LTS + `uv` sebagai package manager (wajib).
- Django latest stable.
- PostgreSQL untuk production, SQLite untuk development/test.
- RDP-UI CDN (`cdn.radian.web.id`) — project membutuhkan akses internet saat development untuk load CDN, atau dikonfigurasi ke local copy.
- django-cotton untuk component system.
- HTMX (via CDN atau static).
- PicoCSS (via CDN atau static).
- WhiteNoise untuk serving static files.
- Gunicorn untuk production WSGI server.

---

## 9. Risks

| Risk | Dampak | Mitigasi |
|---|---|---|
| RDP-UI CDN down atau URL berubah | UI rusak di semua project | Pin versi CDN di `base.html`, sediakan fallback local copy di `static/` |
| Starter kit drift dari project aktif | Standar tidak diikuti, kembali ke masalah awal | Gunakan starter kit untuk minimal 1 project nyata dalam 30 hari pertama sebagai validasi |
| Scope creep — ingin tambah semua fitur opsional ke v0.1 | v0.1 tidak pernah rilis | Pegang hard rule: fitur opsional masuk docs sebagai instruksi, bukan ke template |
| Custom User model salah dikonfigurasi di project baru | Migrasi bermasalah setelah ada data, tidak bisa diubah | Test `migrate` dari database kosong wajib ada di CI |
| Dependency yang lupa dideklarasikan | Gagal install di environment baru | CI wajib install dari `uv sync` di environment bersih, bukan dari cache |

---

## 10. Open Questions

~~1. **Struktur folder**: `apps/` di root — **PUTUSKAN: ✅ `apps/` di root, sesederhana mungkin.**~~

~~2. **Fitur opsional**: Disertakan sebagai kode di-comment atau instruksi di docs? — **PUTUSKAN: ✅ Instruksi di docs saja, tidak ada kode di-comment.**~~

~~3. **Docker**: Masuk v0.1 atau v0.2? — **PUTUSKAN: ✅ Docs saja, tidak ada Dockerfile di v0.1.**~~

~~4. **Adoption target**: Project mana yang pertama? — **PUTUSKAN: ✅ Starter kit ini diselesaikan dulu sebelum dipakai di project real. Tidak butuh migration guide di v0.1.**~~

Semua open questions sudah terjawab. PRD siap naik ke status **Review**.

---

*PRD ini siap untuk Review. Tidak ada blocker tersisa.*
