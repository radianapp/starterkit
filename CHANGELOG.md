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
- **US-017**: Test suite siap pakai — pytest + pytest-django + conftest.py dengan fixtures
- **US-015**: Error pages kustom (403, 404, 500) — template + error handlers
- **US-016**: Security headers production-ready — HSTS, CSP, SECURE_SSL_REDIRECT, dll
- **US-021**: Cache (Redis / Local Memory) — support locmem:// & redis://
- **US-022**: Email (SMTP / Console / Mailpit) — support console, mailpit, SMTP backend
- **US-013**: Static & media files — WhiteNoise + django storage

### Documentation
- README.md — Quick start, project structure, conventions
- CLAUDE.md — AI assistant instructions (sudah ada, di-verify)
- IMPLEMENTATION-PLAN.md — 5 phases, 23 stories, Definition of Done (sudah ada)
- tests/conftest.py — pytest configuration dengan fixtures

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
