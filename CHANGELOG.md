# Changelog

Semua perubahan pada project ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan project ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
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
