# Prompt: Lanjutkan Development RDP Starter Kit dari PRD v0.2

> Salin seluruh isi di bawah garis ini ke sesi AI (Claude Code / Cowork) baru di folder project `starterkit/`.

---

Kamu adalah Senior Solution Software Architect + Developer untuk **RDP Starter Kit**. Project ini sudah berjalan sebagian dan PRD-nya baru dinaikkan ke **v0.2** (`docs/prd/v0.2.md`). Tugasmu: menyelaraskan pekerjaan yang sudah ada dengan PRD v0.2, lalu melanjutkan development story per story.

## Referensi wajib (baca sebelum bekerja)

1. `CLAUDE.md` — konvensi wajib: struktur package per fungsi, `<c-rdp.*>`/`<c-layout.*>`, no inline CSS/JS, `uv` only, referensi US di setiap file.
2. `docs/prd/v0.2.md` — PRD aktif (FR-01 s/d FR-26, 9 layer, Non-Goals). `docs/PRDv0.1.md` hanya arsip.
3. `docs/IMPLEMENTATION-PLAN.md` — status saat ini: Fase 1 selesai kecuali US-016 (security headers); Fase 2 (UI Shell) selesai; Fase 3 (Auth), 4 (Authorization & Admin), 5 (Tooling & Docs) belum.
4. `docs/user-stories/rdp-starter-kit.md` — 23 user story existing (US-001–US-023).
5. `docs/SOP-FRONTEND-STRUCTURE.md` — SOP frontend yang sudah berlaku.
6. Skills di `.claude/`: `rdp-ui`, `django`, `django-cotton`, `htmx`, `user-story`, `development-ai-assisted`, `quality-gate-checklist` — gunakan sesuai tahap.

## Kerjakan berurutan

### Tahap A — Audit gap (jangan menulis kode dulu)

Bandingkan kondisi repo saat ini dengan PRD v0.2. Hasilkan laporan singkat berisi:

- FR mana yang **sudah terpenuhi** oleh kode existing (rujuk file konkret).
- FR mana yang **terpenuhi sebagian** dan apa kurangnya (mis. US-011 sudah membuat komponen dasar — cek terhadap daftar FR-15/FR-16).
- FR mana yang **sama sekali baru** (kandidat: FR-01–FR-03 CLI, FR-06 self-host, FR-07 layout email/print, FR-11, FR-12 public pages, FR-13 demo data dashboard, FR-16 komponen gap, FR-17 confirm dialog, FR-18 halaman demo `/dev/components/`, FR-19 HTMX patterns, FR-20, FR-21 lint template, FR-23–FR-26 docs/SOP).
- Pekerjaan existing yang **bertentangan** dengan v0.2 (jika ada) + usulan penyesuaian.

Tunggu approval KK atas laporan ini sebelum lanjut.

### Tahap B — Update dokumen perencanaan

1. Jalankan skill `user-story`: pecah FR baru dari PRD v0.2 menjadi user story baru, **lanjutkan penomoran dari US-024**. Jangan mengubah isi US-001–US-023. Simpan di `docs/prd/user-stories/rdp-starter-kit.md`.
2. Update `docs/IMPLEMENTATION-PLAN.md`: pertahankan Fase 1–5 beserta statusnya, tambahkan fase baru untuk scope v0.2 (usulan: Fase 6 Layout System & App Shell, Fase 7 Component Library + halaman demo, Fase 8 Public & App Pages + HTMX patterns, Fase 9 CLI & DX, Fase 10 Docs & SOP). Sertakan estimasi poin, prasyarat antar fase, dan file yang akan dibuat.
3. Terapkan FR-23: rapikan `docs/` (`prd/`, `prd/user-stories/`, `sop/`, `cookbook/`, `modules/`, `architecture/`, `decisions/`) dan pindahkan file existing. Update semua path yang merujuknya (CLAUDE.md, skills, README).
4. Update `CLAUDE.md` agar merujuk PRD v0.2 dan struktur docs baru.

### Tahap C — Development

Kerjakan story per story sesuai urutan fase. Prioritas pertama: **US-016** (satu-satunya sisa Fase 1), lalu Fase 3 (Auth) karena FR-09/FR-10 v0.2 bergantung padanya, baru fase-fase baru.

Untuk setiap story, patuhi Definition of Done di `docs/IMPLEMENTATION-PLAN.md`:

- Referensi `US: US-{nomor} — {judul}` di setiap file Python/template yang disentuh.
- `uv run pytest --cov=apps` hijau, coverage ≥ 80%; `uv run ruff check .` bersih; `makemigrations --check --dry-run` bersih.
- Update `CHANGELOG.md` (`[Unreleased]`), ERD `docs/architecture/database.md` jika model berubah, dan `docs/modules/` jika perlu.
- Jika konvensi berubah, update skill terkait di `.claude/` dalam commit yang sama (FR-26).

## Aturan tambahan khusus v0.2

- Komponen gap (table, pagination, tabs, toast, tooltip, accordion, skeleton, empty state, dst.) dibuat sebagai Cotton + CSS di `static/css/components/`, ditulis dengan token `--rdp-*` dan konvensi class `rdp-*` agar siap di-upstream ke RDP-UI v1.1 — jangan menciptakan sistem token sendiri.
- HTMX: error form = HTTP 422 fragment, sukses = `HX-Redirect`, toast = `HX-Trigger`. Semua pattern baru wajib ditambahkan sebagai resep di `docs/cookbook/`.
- Semua yang ada di Non-Goals PRD v0.2 (MFA/OTP, billing, AI components, `create_crud`, dll.) **jangan dikerjakan** meskipun terasa "sekalian".

## Tanyakan ke KK sebelum mengerjakan FR terkait (Open Questions PRD v0.2)

1. Bentuk distribusi CLI `rdp new` (uv tool standalone vs script dalam repo) → blokir FR-01/FR-02.
2. Mekanisme & kriteria upstream komponen ke RDP-UI v1.1 → memengaruhi FR-16.
3. Path CDN berversi dari RDP-UI → memengaruhi FR-05/FR-06.

Mulai dari **Tahap A** sekarang dan laporkan hasil auditnya.
