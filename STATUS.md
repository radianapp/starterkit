# Project Status

*Cara baca/update: Tambahkan status terbaru di paling atas dari daftar timeline (di bawah header).*

---

## 📈 Overall Progress: ~80% (v0.2 In Progress)

- Project saat ini berada di tahapan akhir penyelesaian versi 0.2. 
- Sebagian besar User Stories (US-001 hingga US-042) telah diimplementasikan secara kode (Fase 1 s/d Fase 10).
- Fokus saat ini adalah menyelesaikan proses *Definition of Done* (DoD), integrasi akhir, penambahan test/coverage, perapihan UI template, dan finalisasi dokumen agar mencapai milestone 100%.

---

## 📅 Timeline Kegiatan

### Fase 10 — Dokumentasi & SOP (In Progress)
- [x] US-039: Restrukturisasi `docs/` sesuai standar v0.2
- [x] US-040: SOP lengkap — HTMX, Cotton, Git, testing, modul
- [x] US-041: Cookbook resep langkah-demi-langkah
- [x] US-042: Workflow update skills AI seiring perubahan konvensi
- **Status Akhir**: Kebutuhan konten dasar sudah ada, tetapi perlu checklist penyelesaian standar *Definition of Done* (seperti pengecekan tautan dokumen, testing script deployment secara menyeluruh).

### Fase 9 — CLI & DX (Selesai)
- [x] US-024: CLI `rdp new` — wizard interaktif bootstrap project (tersedia secara global via `uv tool install`)
- [x] US-025: Template app untuk `manage.py startapp --template` (termasuk folder struktur apps)
- [x] US-037: Management command demo data (`loaddemodata`)
- [x] US-038: Script lint template + integrasi CI (`scripts/lint_templates.py`)

### Fase 8 — Public & App Pages + HTMX Patterns (Selesai)
- [x] US-029: HTMX form validation pattern (`HtmxFormMixin`)
- [x] US-030: Layout email + template email transaksional
- [x] US-031: Public pages — landing, about, terms, privacy
- [x] US-032: Dashboard default dengan demo data & tabel pagination HTMX
- [x] US-036: 10 HTMX patterns — contoh hidup + resep cookbook di `/examples/htmx/`

### Fase 7 — Component Library (Selesai)
- [x] US-033: Komponen Cotton RDP-UI v1.0 gap (badge, avatar, loader)
- [x] US-034: Component library gap (tabs, toast, tooltip, accordion, skeleton, dll)
- [x] US-035: Halaman demo komponen internal `/dev/components/`

### Fase 6 — Layout System & App Shell (Selesai)
- [x] US-026: Self-host RDP-UI aset via env var
- [x] US-027: Layout system lengkap (7 layout utama tanpa inline CSS)
- [x] US-028: App shell lengkap (persistent theme via localStorage, toast & modal global)

### Fase 5 — Tooling & Dokumentasi (Selesai)
- [x] US-018: CI/CD GitHub Actions
- [x] US-019: CLAUDE.md untuk AI assistant
- [x] US-023: Dokumentasi project (getting-started, configuration, cookbook, faq)

### Fase 4 — Authorization & Admin (Selesai)
- [x] US-020: Authorization (Permission & Group) (custom mixin & unit tests)
- [x] US-012: Admin Django kustom (tema darkly, search custom, topmenu custom)

### Fase 3 — Authentication (Selesai)
- [x] US-004: Register akun baru (multi-step wizard + batasan email domain via .env)
- [x] US-005: Login (form HTMX-aware, redirect guard)
- [x] US-006: Logout
- [x] US-007: Lupa password & reset
- [x] US-008: Verifikasi email (token 72 jam via signing)
- [x] US-009: Edit profil & avatar (upload JPG/PNG/WebP maks 2MB, preview instan)

### Fase 2 — UI Shell (Selesai)
- [x] US-010: Layout dasar (navbar, sidebar, dashboard, dark mode toggle)
- [x] US-011: Komponen UI dasar (button, card, alert, modal, form, dll)
- [x] US-015: Error pages kustom (403, 404, 500 ter-styling)

### Fase 1 — Fondasi (Selesai)
- [x] US-001: Clone & jalankan project baru
- [x] US-002: Konfigurasi environment via `.env`
- [x] US-003: Custom User model siap pakai (extend AbstractUser, UserProfile)
- [x] US-016: Security headers production-ready
- [x] US-021: Cache (Redis / Local Memory)
- [x] US-022: Email (SMTP / Console / Mailpit)
- [x] US-013: Static & media files (WhiteNoise)
- [x] US-014: Logging terstruktur
- [x] US-017: Test suite siap pakai (pytest + conftest)
