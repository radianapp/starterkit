# User Guide: Testing US-016 — Security Headers

## Apa yang Diuji?

US-016 memastikan production settings Django sudah dikonfigurasi dengan security headers yang benar:

| Header | Setting Django | Nilai |
|---|---|---|
| `Strict-Transport-Security` | `SECURE_HSTS_SECONDS` | 31536000 (1 tahun) |
| `X-Frame-Options` | `X_FRAME_OPTIONS` | `DENY` |
| `X-Content-Type-Options` | `SECURE_CONTENT_TYPE_NOSNIFF` | `True` |
| `Referrer-Policy` | `SECURE_REFERRER_POLICY` | `strict-origin-when-cross-origin` |
| SSL redirect | `SECURE_SSL_REDIRECT` | `True` |
| Session cookie | `SESSION_COOKIE_SECURE` | `True` |
| CSRF cookie | `CSRF_COOKIE_SECURE` | `True` |

---

## Cara 1: Automated Tests (Direkomendasikan)

```bash
# Jalankan test security saja
uv run pytest tests/test_security.py -v

# Atau semua tests
uv run pytest -v
```

Output yang diharapkan: **15 passed** tanpa error.

---

## Cara 2: Django Deploy Check

Django punya built-in checker untuk production settings:

```bash
uv run python manage.py check --deploy --settings=config.settings.production
```

Output normal (bukan error):
```
System check identified no issues (0 silenced).
```

Jika ada warning, kemungkinan besar soal CSP (Content Security Policy) — ini sudah didokumentasikan sebagai roadmap v0.3 menggunakan `django-csp`.

---

## Cara 3: Manual — Simulasi Production Settings Lokal

Untuk verifikasi header HTTP actual di browser:

```bash
# Set env variable, lalu run dev server dengan production settings
$env:DJANGO_SETTINGS_MODULE="config.settings.production"
$env:ALLOWED_HOSTS="localhost"
$env:SECRET_KEY="test-key-for-local-check-only"
$env:DATABASE_URL="sqlite:///db.sqlite3"

uv run python manage.py runserver --insecure
```

> **Catatan:** `SECURE_SSL_REDIRECT=True` di production settings akan redirect semua HTTP ke HTTPS. Karena localhost tidak pakai HTTPS, server mungkin langsung redirect dan tidak bisa diakses normal. Cara termudah tetap automated tests (Cara 1).

---

## Cara 4: Browser DevTools

Setelah server running (gunakan dev settings biasa untuk browser check), buka halaman apapun:

1. Buka DevTools → tab **Network**
2. Klik request apapun (misalnya `/dashboard/`)
3. Lihat tab **Headers** → bagian **Response Headers**

Header yang akan terlihat di **development** (dev settings):

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
```

Header yang hanya muncul di **production** (butuh HTTPS):

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
```

---

## Pengecekan Ruff (Code Quality)

```bash
uv run ruff check .
```

Output yang diharapkan: `All checks passed!`

---

## Ringkasan Hasil US-016

- **15 automated tests** — semua passing
- **Ruff** — 0 errors
- **`SECURE_CONTENT_SECURITY_POLICY`** (dead code) sudah dihapus
- **CSP** → roadmap v0.3 via `django-csp` (dicatat di komentar production.py)
- Coverage: 68% overall (naik dari baseline sebelumnya)
