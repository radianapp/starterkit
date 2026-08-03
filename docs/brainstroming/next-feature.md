# Rencana Implementasi Lanjutan (RDP Enterprise Features)

Dokumen ini memuat usulan desain arsitektur dan tahapan eksekusi untuk melengkapi RDP Starter Kit menuju standar *Enterprise-Grade*. Semua fitur besar ini dirancang agar bersifat *pluggable* (bisa dimatikan/dinyalakan via `.env`) untuk menjaga starter kit tetap ringan jika fitur tersebut tidak dibutuhkan.

> [!IMPORTANT]
> **User Review Required**
> Mohon tinjau rencana di bawah ini. Anda bisa memberi masukan, menentukan prioritas (mana yang harus dikerjakan lebih dulu), atau menyetujui seluruhnya agar saya bisa mulai mengeksekusinya secara bertahap.

---

## 1. Pengujian Otomatis (TDD & Test Coverage)
Menerapkan budaya *Test-Driven Development* secara menyeluruh di seluruh aplikasi.

*   **Peralatan:** `pytest`, `pytest-django`, `pytest-cov`.
*   **Target:** 
    *   Mencapai *code coverage* > 80% (terutama di direktori `apps/`).
    *   Membuat *test suite* yang mencakup unit test (models/services), integration test (views/htmx), dan form validation.
*   **Implementasi:**
    *   [NEW] Konfigurasi `pytest.ini` dan `.coveragerc` di root project.
    *   [NEW] Menambahkan `tests/` di `apps/accounts/`, `apps/inventory/`, dll.
    *   [MODIFY] Mengupdate `pyproject.toml` untuk skrip otomatis (misal: `uv run pytest`).

## 2. Role-Based Access Control (RBAC) Dinamis
Menggantikan otorisasi sederhana `is_staff` dengan sistem Peran (Roles) dan Izin (Permissions) yang dinamis.

*   **Peralatan:** Menggunakan kombinasi `Group` dan `Permission` bawaan Django yang diperluas.
*   **Target:** Menyediakan roles default seperti `SuperAdmin`, `Admin`, `Editor`, dan `Viewer`.
*   **Implementasi:**
    *   [NEW] Membuat `apps/accounts/services/rbac_service.py` untuk inisialisasi default roles.
    *   [NEW] Membuat kustom *decorators* (misal: `@role_required('Editor')`) dan *mixins* untuk CBV.
    *   [MODIFY] Menambahkan tabel/UI manajemen *Role* dan *User Assignment* di halaman Admin Panel / Dashboard.

## 3. Audit Trail (Log Aktivitas Pengguna)
Mencatat historis perubahan data (CRUD) secara terpusat. Fitur ini dapat diatur melalui `.env`.

*   **Peralatan:** `django-simple-history` atau `django-auditlog`.
*   **Target:** Jika `ENABLE_AUDIT_TRAIL=True`, setiap perubahan pada model penting (seperti Produk, User, Transaksi) akan otomatis dicatat beserta pengguna yang mengubah dan alamat IP-nya.
*   **Implementasi:**
    *   [MODIFY] Menambahkan `ENABLE_AUDIT_TRAIL` di `.env` dan `base.py`.
    *   [MODIFY] Mendaftarkan model-model yang akan dilacak ke sistem *history*.
    *   [NEW] Membuat halaman di Dashboard untuk melihat log aktivitas.

## 4. Background Tasks (Celery / Redis)
Memisahkan proses berat (I/O blocking) dari *request-response cycle* utama HTTP.

*   **Peralatan:** `celery`, `redis` (sebagai broker & backend).
*   **Target:** Pemrosesan email, pembuatan laporan, dan notifikasi diproses secara *asynchronous*.
*   **Implementasi:**
    *   [NEW] Membuat `config/celery.py`.
    *   [MODIFY] Mengubah `apps/accounts/services/user_service.py` agar pemanggilan `send_mail` menggunakan task Celery (misal: `send_verification_email_task.delay()`).
    *   [MODIFY] Menambahkan konfigurasi broker di `.env` (misal: `CELERY_BROKER_URL`).

## 5. Integrasi API Murni (Django REST Framework)
Menyediakan endpoint JSON yang standar untuk konsumsi pihak ketiga atau aplikasi mobile.

*   **Peralatan:** `djangorestframework`, `drf-spectacular` (untuk Swagger/OpenAPI).
*   **Target:** Endpoint API terisolasi di bawah rute `/api/v1/`.
*   **Implementasi:**
    *   [NEW] Membuat direktori `api/` di dalam tiap aplikasi (misal: `apps/inventory/api/`).
    *   [NEW] Membuat `serializers.py` dan `views.py` (menggunakan `ViewSet`).
    *   [MODIFY] Registrasi rute API ke `config/api_urls.py`.

## 6. Security & Hardening (termasuk 2FA/MFA)
Memperkuat keamanan aplikasi untuk standar korporat (diatur via `.env`).

*   **Peralatan:** Fitur MFA dari `django-allauth` (karena allauth baru saja kita pasang).
*   **Target:**
    *   `REQUIRE_2FA=True`: Memaksa pengguna untuk setup TOTP (Google Authenticator) setelah login sukses.
    *   Rotasi Kata Sandi (opsional): Menambahkan *field* `password_last_updated` di model User untuk memaksa pembaruan setelah 90 hari.
*   **Implementasi:**
    *   [MODIFY] Integrasi halaman *setup* 2FA ke dalam profil atau alur login (Login -> Cek 2FA -> Dashboard).
    *   [MODIFY] Menambahkan middleware `PasswordRotationMiddleware` jika diaktifkan.

---

> [!TIP]
> **Rekomendasi Prioritas Eksekusi**
> Karena ukuran rencananya cukup besar, saya menyarankan pendekatan fase (berurutan):
> 1. **Fase 1**: Audit Trail & RBAC (Sangat mempengaruhi struktur database dasar).
> 2. **Fase 2**: Background Tasks & Integrasi API.
> 3. **Fase 3**: Security/MFA & Pengujian (TDD) untuk membungkus semuanya dengan aman.
> 
> *Apakah Anda setuju dengan urutan ini, atau ada satu fitur yang ingin difokuskan terlebih dahulu?*
