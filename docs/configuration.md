# Konfigurasi Project (Configuration Guide)
<!-- US: US-023 — Dokumentasi project -->

Seluruh konfigurasi sensitif dan modular diatur menggunakan environment variables dalam file `.env` di root project.

## Daftar Variabel Lingkungan (.env)

Berikut penjelasan variabel yang dapat dikonfigurasi:

### 1. Keamanan & Inti Django
| Nama Variabel | Tipe Data | Deskripsi | Default (Dev) | Rekomendasi Prod |
|---|---|---|---|---|
| `SECRET_KEY` | String | Key rahasia enkripsi Django. | `django-insecure-...` | Ganti dengan string acak dan panjang |
| `DEBUG` | Boolean | Mengaktifkan mode debug Django. | `True` | `False` |
| `ALLOWED_HOSTS` | List (Comma) | Host/domain yang diizinkan memproses request. | `localhost,127.0.0.1` | Domain Anda (mis. `app.radian.web.id`) |
| `ENVIRONMENT` | String | Nama environment yang berjalan. | `development` | `production` |

### 2. Branding (White Label)
| Nama Variabel | Tipe Data | Deskripsi | Default |
|---|---|---|---|
| `SITE_NAME` | String | Nama situs lengkap. | `RDP Starter Kit` |
| `COMPANY_NAME` | String | Nama organisasi/perusahaan pemilik. | `Radian Data Platform` |
| `APP_BRAND_SHORT` | String | Singkatan nama aplikasi/brand di header. | `RDP` |

### 3. Database & Caching
| Nama Variabel | Tipe Data | Deskripsi | Default | Rekomendasi Prod |
|---|---|---|---|---|
| `DATABASE_URL` | String | URL koneksi ke DB. | `sqlite:///db.sqlite3` | `postgresql://user:pass@host:port/dbname` |
| `CACHE_URL` | String | URL koneksi cache Django. | `locmem://` | `redis://127.0.0.1:6379/0` |

### 4. Layanan Email
| Nama Variabel | Tipe Data | Deskripsi | Pilihan Nilai |
|---|---|---|---|
| `EMAIL_BACKEND` | String | Backend pengiriman email yang aktif. | `console` (dev), `mailpit` (local-test), `smtp` (prod) |
| `EMAIL_HOST` | String | Host SMTP Server (jika smtp). | Contoh: `smtp.gmail.com` |
| `EMAIL_PORT` | Integer | Port SMTP Server. | Contoh: `587` |
| `EMAIL_USE_TLS` | Boolean | Gunakan proteksi TLS. | `True` / `False` |
| `EMAIL_HOST_USER` | String | User autentikasi SMTP. | - |
| `EMAIL_HOST_PASSWORD` | String | Password/App-token SMTP. | - |
| `DEFAULT_FROM_EMAIL` | String | Alamat pengirim bawaan. | `noreply@radianapp.com` |

### 5. Fitur Autentikasi Tambahan
| Nama Variabel | Tipe Data | Deskripsi | Pilihan Nilai |
|---|---|---|---|
| `REQUIRE_EMAIL_VERIFICATION` | Boolean | Wajib verifikasi email untuk membuka akses penuh. | `True` / `False` |
| `REGISTRATION_STEPS` | JSON String | Pengaturan wizard multi-step registrasi. | `[]` (kosong berarti wizard email+password biasa) |

---

## Memverifikasi Konfigurasi di Production

Saat deploy ke production, pastikan Anda menjalankan perintah pengujian konfigurasi Django berikut untuk meminimalkan celah keamanan:

```bash
uv run python manage.py check --deploy
```
