# User Stories — RDP Starter Kit

**Sumber PRD**: docs/prd/v0.1.md  
**Tanggal**: 2026-06-29  
**Persona**: KK — Solo Founder / Lead Developer RDP

---

## US-001: Clone & jalankan project baru

**Story**:  
Sebagai developer, saya ingin bisa clone starter kit dan langsung menjalankan `runserver` hanya dengan menyalin `.env.example`, sehingga saya tidak membuang waktu setup manual yang berulang.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given repo sudah di-clone dan `.env.example` disalin ke `.env`, When developer menjalankan `uv sync && uv run python manage.py migrate && uv run python manage.py runserver`, Then server berjalan di `localhost:8000` tanpa error dalam < 5 menit.
- Given server sudah berjalan, When developer membuka `http://localhost:8000`, Then halaman dashboard/landing muncul tanpa error.
- Given `.env.example`, When developer membukanya, Then semua variabel wajib (SECRET_KEY, DATABASE_URL, DEBUG) sudah ada dengan nilai default yang aman untuk development.

**Dependencies**: —

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-002: Konfigurasi environment via `.env`

**Story**:  
Sebagai developer, saya ingin semua konfigurasi sensitif dibaca dari file `.env`, sehingga tidak ada credential yang ter-hardcode di kode dan aman untuk di-commit ke git.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given file `.env` sudah diisi, When Django startup, Then semua nilai (SECRET_KEY, DATABASE_URL, EMAIL_*, CACHE_URL) terbaca dari env tanpa error.
- Given developer menghapus `SECRET_KEY` dari `.env`, When Django startup, Then aplikasi raise error eksplisit yang menyebut variabel yang hilang, bukan `ImproperlyConfigured` yang samar.
- Given repository di-clone di environment baru tanpa `.env`, When developer menjalankan `git grep SECRET_KEY`, Then tidak ada nilai hardcoded di file Python manapun.

**Dependencies**: US-001

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-003: Custom User model siap pakai

**Story**:  
Sebagai developer, saya ingin `AUTH_USER_MODEL` sudah dikonfigurasi dengan Custom User model sejak awal, sehingga saya bisa menambahkan field ke User kapan saja tanpa risiko migrasi berbahaya.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given project baru di-clone, When developer menjalankan `uv run python manage.py migrate` di database kosong, Then migrasi selesai tanpa error dan `AUTH_USER_MODEL` menunjuk ke `accounts.User`.
- Given `accounts.User` sudah ada, When developer menambahkan field baru ke model dan menjalankan `makemigrations`, Then migrasi baru terbuat tanpa konflik.
- Given `AUTH_USER_MODEL = "accounts.User"` di `settings/base.py`, When developer menjalankan `python manage.py check`, Then tidak ada warning tentang User model.

**Dependencies**: US-001

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-004: Register akun baru

**Story**:  
Sebagai pengguna, saya ingin mendaftar akun baru dengan email dan password, sehingga saya bisa mengakses aplikasi.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given halaman register, When pengguna mengisi email valid dan password yang memenuhi syarat lalu submit, Then akun dibuat dan pengguna di-redirect ke halaman konfirmasi atau dashboard.
- Given halaman register, When pengguna mengisi email yang sudah terdaftar, Then muncul pesan error yang jelas tanpa membocorkan apakah email tersebut terdaftar atau tidak.
- Given form register, When pengguna submit dengan field kosong atau password tidak cocok, Then form menampilkan pesan error per field tanpa full page reload (response HTMX 422).
- Given register berhasil dengan email verification aktif, When akun dibuat, Then email verifikasi terkirim ke alamat yang didaftarkan.

**Dependencies**: US-002, US-003

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-005: Login

**Story**:  
Sebagai pengguna terdaftar, saya ingin login dengan email dan password, sehingga saya bisa mengakses fitur yang membutuhkan autentikasi.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given halaman login, When pengguna mengisi email dan password yang benar lalu submit, Then pengguna di-redirect ke dashboard.
- Given halaman login, When pengguna mengisi email atau password yang salah, Then muncul pesan error umum (bukan menyebut field mana yang salah) dan form tetap tampil.
- Given pengguna belum login, When mengakses URL yang butuh autentikasi, Then di-redirect ke halaman login dengan next parameter yang benar.
- Given form login, When submit dengan HTMX, Then response menggunakan HX-Redirect untuk sukses atau fragment error untuk gagal — bukan full page reload.

**Dependencies**: US-003, US-004

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-006: Logout

**Story**:  
Sebagai pengguna yang sudah login, saya ingin bisa logout, sehingga sesi saya berakhir dengan aman.

**Prioritas**: Must  
**Estimasi**: 1

**Acceptance Criteria**:
- Given pengguna sudah login, When pengguna mengklik tombol logout, Then sesi dihapus dan pengguna di-redirect ke halaman login.
- Given pengguna sudah logout, When mencoba mengakses halaman yang butuh autentikasi, Then di-redirect ke halaman login.
- Given tombol logout, When diklik, Then request menggunakan method POST (bukan GET) untuk mencegah logout via link eksternal.

**Dependencies**: US-005

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-007: Lupa password & reset

**Story**:  
Sebagai pengguna yang lupa password, saya ingin meminta link reset password via email, sehingga saya bisa mengakses akun saya kembali.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given halaman forgot password, When pengguna mengisi email terdaftar dan submit, Then email berisi link reset terkirim dan muncul pesan konfirmasi.
- Given halaman forgot password, When pengguna mengisi email yang tidak terdaftar, Then muncul pesan yang sama (tidak membocorkan status email).
- Given link reset di email, When diklik dalam 24 jam, Then pengguna diarahkan ke form set password baru.
- Given link reset, When digunakan lebih dari satu kali atau sudah expired, Then muncul pesan error yang jelas dan pengguna diarahkan ke forgot password page.

**Dependencies**: US-002, US-005

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-008: Verifikasi email

**Story**:  
Sebagai pengguna baru, saya ingin memverifikasi email saya setelah register, sehingga akun saya terverifikasi dan akses fitur penuh terbuka.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given register berhasil, When pengguna membuka email dan mengklik link verifikasi, Then akun ditandai `email_verified=True` dan pengguna di-redirect ke dashboard.
- Given link verifikasi, When diklik lebih dari sekali, Then tetap berhasil (idempotent) atau muncul pesan "sudah terverifikasi" yang ramah.
- Given link verifikasi expired (> 72 jam), When diklik, Then muncul opsi untuk kirim ulang email verifikasi.
- Given pengguna belum verifikasi email dan fitur verifikasi wajib aktif, When mencoba akses fitur tertentu, Then diarahkan ke halaman "cek email kamu".

**Dependencies**: US-004, US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-009: Edit profil & avatar

**Story**:  
Sebagai pengguna yang sudah login, saya ingin mengedit nama dan foto profil saya, sehingga akun saya mencerminkan identitas saya.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given halaman profil, When pengguna mengubah nama dan menyimpan, Then nama terupdate dan muncul pesan sukses.
- Given halaman profil, When pengguna mengupload foto (JPG/PNG, maks 2MB), Then foto tersimpan dan tampil sebagai avatar di navbar.
- Given upload foto > 2MB atau format bukan gambar, When disimpan, Then muncul pesan error yang jelas.
- Given pengguna belum upload avatar, When melihat profil atau navbar, Then tampil avatar default (inisial nama atau placeholder).

**Dependencies**: US-005, US-003

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-010: Layout dasar (navbar, sidebar, dashboard)

**Story**:  
Sebagai developer, saya ingin template layout dasar (navbar, sidebar, dashboard, settings page) sudah tersedia sebagai komponen Cotton, sehingga saya bisa langsung membangun halaman tanpa mendesain ulang struktur dari nol.

**Prioritas**: Must  
**Estimasi**: 5

**Acceptance Criteria**:
- Given project baru, When developer membuat template baru dan mengextend `base.html`, Then navbar dan sidebar tampil secara otomatis.
- Given `base.html`, When dirender di browser, Then RDP-UI CDN + PicoCSS + HTMX + Alpine.js sudah ter-load.
- Given komponen `<c-rdp.layout.navbar>` dan `<c-rdp.layout.sidebar>`, When developer perlu menyesuaikan, Then bisa di-override di folder `templates/cotton/` project tanpa mengubah starter kit.
- Given halaman apapun yang menggunakan `base.html`, When dibuka di browser dalam dark mode OS, Then tampilan mengikuti dark mode via RDP-UI otomatis.

**Dependencies**: US-001, US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-011: Komponen UI dasar

**Story**:  
Sebagai developer, saya ingin komponen UI umum (button, card, alert, modal, table, form, pagination, breadcrumb, dropdown) tersedia sebagai komponen Cotton, sehingga saya tidak perlu menulis HTML yang sama berulang kali.

**Prioritas**: Must  
**Estimasi**: 5

**Acceptance Criteria**:
- Given komponen `<c-rdp.button variant="primary">`, When dirender, Then tampil button dengan styling RDP-UI yang benar dan mendukung atribut HTMX (`hx-post`, `hx-target`, dll.) secara transparan.
- Given komponen `<c-rdp.alert type="error">`, When dirender dengan slot content, Then tampil alert dengan warna dan ikon yang sesuai tipe.
- Given komponen `<c-rdp.modal>`, When trigger diklik, Then modal terbuka tanpa JavaScript kustom (cukup HTMX atau Alpine.js).
- Given komponen `<c-rdp.table>`, When dirender dengan data, Then tampil tabel responsif yang mengikuti styling PicoCSS + RDP-UI.
- Given semua komponen, When developer menggunakan atribut yang tidak dikenali, Then atribut di-pass-through ke elemen HTML dasar (tidak diabaikan diam-diam).

**Dependencies**: US-010

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-012: Admin Django kustom

**Story**:  
Sebagai developer, saya ingin Admin Django sudah dikustomisasi dengan tampilan yang lebih baik, search, filter, dan dark mode, sehingga saya bisa langsung pakai untuk operasional tanpa setup tambahan.

**Prioritas**: Should  
**Estimasi**: 3

**Acceptance Criteria**:
- Given developer membuka `/admin/`, When login sebagai superuser, Then tampil admin dengan tema kustom (bukan tema Django default bawaan).
- Given admin panel, When system OS dalam dark mode, Then admin mengikuti dark mode secara otomatis.
- Given model yang didaftarkan di admin, When developer membuka list view, Then search dan filter tersedia sesuai field yang dikonfigurasi.
- Given `python manage.py createsuperuser`, When selesai dan login ke admin, Then semua fungsi admin berjalan normal.

**Dependencies**: US-003

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-013: Static & media files

**Story**:  
Sebagai developer, saya ingin static dan media files terlayani otomatis (WhiteNoise untuk static, local/S3 untuk media), sehingga tidak perlu konfigurasi nginx tambahan di fase awal.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given `DEBUG=False` di `.env`, When server dijalankan dengan Gunicorn, Then static files terlayani via WhiteNoise tanpa konfigurasi web server tambahan.
- Given `MEDIA_BACKEND=local` di `.env`, When user upload file, Then file tersimpan di folder `media/` lokal.
- Given `MEDIA_BACKEND=s3` dan variabel S3 terisi di `.env`, When user upload file, Then file tersimpan di S3-compatible storage tanpa mengubah kode aplikasi.
- Given `python manage.py collectstatic`, When dijalankan, Then semua static file terkumpul ke `staticfiles/` tanpa error.

**Dependencies**: US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-014: Logging terstruktur

**Story**:  
Sebagai developer, saya ingin logging aktif by default dengan format yang berbeda untuk development dan production, sehingga saya bisa debug dengan mudah di dev dan parse log di production.

**Prioritas**: Should  
**Estimasi**: 2

**Acceptance Criteria**:
- Given `DEBUG=True`, When request masuk, Then log tampil di console dalam format human-readable.
- Given `DEBUG=False`, When request masuk atau terjadi error, Then log ditulis ke file `logs/app.log` dalam format JSON.
- Given exception yang tidak ditangkap di view, When terjadi, Then error ter-log dengan traceback lengkap (tidak hanya pesan error).
- Given level logging di `.env` (`LOG_LEVEL=WARNING`), When dikonfigurasi, Then hanya log dengan level tersebut ke atas yang ditulis.

**Dependencies**: US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-015: Error pages kustom (403, 404, 500)

**Story**:  
Sebagai pengguna, saya ingin halaman error (403, 404, 500) memiliki tampilan yang konsisten dengan aplikasi, sehingga pengalaman tidak rusak saat terjadi error.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given user mengakses URL yang tidak ada, When Django mengembalikan 404, Then tampil halaman 404 kustom dengan layout yang konsisten (navbar, branding) — bukan halaman default Django.
- Given user mengakses halaman yang tidak punya izin, When Django mengembalikan 403, Then tampil halaman 403 kustom dengan pesan yang jelas.
- Given terjadi server error (500), When Django mengembalikan 500, Then tampil halaman 500 kustom yang tidak mengekspos stack trace ke user.
- Given `DEBUG=False`, When semua halaman error di-test, Then halaman kustom yang tampil (bukan debug page Django).

**Dependencies**: US-010

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-016: Security headers production-ready

**Story**:  
Sebagai developer, saya ingin security headers (CSP, HSTS, CSRF, secure cookie) sudah aktif by default di production settings, sehingga project baru tidak punya celah keamanan umum sejak hari pertama.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given `settings/production.py` aktif, When server merespons request, Then header `Strict-Transport-Security`, `X-Content-Type-Options`, dan `X-Frame-Options` ada di response.
- Given `settings/production.py`, When diperiksa, Then `DEBUG = False`, `SECURE_SSL_REDIRECT = True`, `SESSION_COOKIE_SECURE = True`, dan `CSRF_COOKIE_SECURE = True` sudah ter-set.
- Given `python manage.py check --deploy`, When dijalankan di production settings, Then tidak ada warning kritis yang tersisa.
- Given `settings/dev.py`, When dipakai di development, Then security redirect (HTTPS) tidak aktif agar tidak mengganggu local dev.

**Dependencies**: US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-017: Test suite siap pakai

**Story**:  
Sebagai developer, saya ingin `uv run pytest` langsung lulus 100% setelah clone, sehingga saya bisa mulai menulis test baru dengan fondasi yang sudah bersih.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given project baru di-clone dan `.env` sudah di-setup, When developer menjalankan `uv run pytest`, Then semua test lulus dan coverage report terbuat.
- Given `pytest.ini` atau konfigurasi di `pyproject.toml`, When pytest dijalankan, Then test discovery berjalan otomatis tanpa flag tambahan.
- Given `uv run pytest --cov=apps`, When dijalankan, Then coverage report menampilkan persentase coverage untuk setiap app.
- Given project baru, When developer melihat struktur `tests/`, Then ada contoh test (smoke test) yang bisa dijadikan referensi pola penulisan test.

**Dependencies**: US-001, US-003

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-018: CI/CD GitHub Actions

**Story**:  
Sebagai developer, saya ingin GitHub Actions sudah terkonfigurasi untuk lint, test, dan migration check pada setiap push, sehingga kualitas kode terjaga otomatis sejak commit pertama.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given developer push ke GitHub, When Actions berjalan, Then pipeline lint (Ruff) → test (Pytest) → migration check berjalan secara berurutan.
- Given ada kode yang tidak lolos Ruff, When push, Then pipeline gagal di step lint dan tidak melanjutkan ke step berikutnya.
- Given ada test yang gagal, When push, Then pipeline gagal di step test dengan output error yang jelas.
- Given developer lupa membuat file migrasi setelah mengubah model, When push, Then migration check gagal dengan pesan yang menyebut migration yang belum dibuat.
- Given push pertama ke repo baru yang dibuat dari starter kit, When Actions berjalan, Then pipeline hijau tanpa konfigurasi tambahan.

**Dependencies**: US-017

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-019: CLAUDE.md untuk AI assistant

**Story**:  
Sebagai developer yang menggunakan AI assistant (Claude), saya ingin ada `CLAUDE.md` di root project yang menjelaskan struktur dan konvensi project, sehingga AI assistant bisa langsung memberi saran yang relevan tanpa perlu orientasi panjang.

**Prioritas**: Should  
**Estimasi**: 1

**Acceptance Criteria**:
- Given project baru di-clone, When developer atau AI assistant membuka `CLAUDE.md`, Then tersedia: deskripsi project, struktur folder, konvensi naming, tech stack, dan cara jalankan dev server + test.
- Given `CLAUDE.md` sudah ada, When developer meminta Claude untuk "buat view baru untuk fitur X", Then Claude mengikuti pola yang ada di project (folder structure, naming) tanpa perlu diarahkan ulang.
- Given `CLAUDE.md`, When dibaca, Then tidak ada instruksi yang sudah outdated atau bertentangan dengan kode yang ada.

**Dependencies**: US-001

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

---

## US-020: Authorization (Permission & Group)

**Story**:  
Sebagai developer, saya ingin permission dan group Django sudah terkonfigurasi dengan mixin/decorator siap pakai, sehingga saya bisa langsung mengontrol akses per view tanpa setup tambahan.

**Prioritas**: Must  
**Estimasi**: 3

**Acceptance Criteria**:
- Given view yang dilindungi dengan `@permission_required("app.can_do_x")`, When user tanpa permission mengakses, Then di-redirect ke halaman 403.
- Given user yang di-assign ke group tertentu, When login dan mengakses view yang membutuhkan permission dari group tersebut, Then akses diberikan.
- Given starter kit, When developer membuka contoh kode di `apps/core/`, Then ada contoh penggunaan `PermissionRequiredMixin` dan `@permission_required` yang bisa langsung dijadikan referensi.
- Given admin panel, When superuser membuka manajemen user, Then bisa assign permission dan group ke user via interface admin.

**Dependencies**: US-003, US-005, US-012

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-021: Cache (Redis / Local Memory)

**Story**:  
Sebagai developer, saya ingin cache sudah terkonfigurasi via env dan bisa swap antara Redis dan local memory tanpa mengubah kode, sehingga development bisa jalan tanpa Redis dan production otomatis pakai Redis.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given `CACHE_URL=locmem://` di `.env`, When Django startup, Then cache backend menggunakan local memory — tidak butuh Redis terinstall.
- Given `CACHE_URL=redis://localhost:6379/0` di `.env`, When Django startup, Then cache backend menggunakan Redis.
- Given swap `CACHE_URL` di `.env`, When server restart, Then backend cache berubah tanpa mengubah satu baris kode Python.
- Given developer menggunakan `from django.core.cache import cache`, When memanggil `cache.set()` dan `cache.get()`, Then berfungsi dengan backend apapun yang dikonfigurasi.

**Dependencies**: US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-022: Email (SMTP / Console / Mailpit)

**Story**:  
Sebagai developer, saya ingin email backend bisa di-swap via env antara console (dev), Mailpit (test HTML), dan SMTP (production), sehingga tidak perlu kirim email sungguhan saat development.

**Prioritas**: Must  
**Estimasi**: 2

**Acceptance Criteria**:
- Given `EMAIL_BACKEND=console` di `.env`, When aplikasi mengirim email, Then email muncul di terminal — tidak ada email terkirim ke luar.
- Given `EMAIL_BACKEND=mailpit` dan Mailpit berjalan di `localhost:1025`, When aplikasi mengirim email, Then email bisa dilihat di Mailpit web UI (`localhost:8025`) dengan layout HTML yang benar.
- Given `EMAIL_BACKEND=smtp` dan variabel SMTP terisi di `.env`, When aplikasi mengirim email, Then email terkirim via SMTP server yang dikonfigurasi.
- Given swap `EMAIL_BACKEND` di `.env`, When server restart, Then backend email berubah tanpa mengubah kode Python.

**Dependencies**: US-002

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-023: Dokumentasi project

**Story**:  
Sebagai developer baru yang clone starter kit, saya ingin ada dokumentasi lengkap di folder `docs/`, sehingga saya bisa mulai produktif tanpa harus membaca source code dari awal.

**Prioritas**: Should  
**Estimasi**: 3

**Acceptance Criteria**:
- Given folder `docs/`, When developer membukanya, Then tersedia setidaknya: `getting-started.md`, `configuration.md`, `faq.md`, dan `cookbook.md`.
- Given `docs/getting-started.md`, When dibaca, Then developer bisa menjalankan project dari clone sampai `runserver` hanya mengikuti langkah-langkah di dokumen tersebut.
- Given `docs/configuration.md`, When dibaca, Then semua variabel `.env` terdokumentasi dengan nama, tipe, nilai default, dan contoh nilai production.
- Given `docs/cookbook.md`, When dibaca, Then tersedia resep: cara tambah Django app baru, cara aktifkan Celery, cara aktifkan ASGI, cara switch ke S3.
- Given `docs/faq.md`, When dibaca, Then menjawab minimal 5 pertanyaan umum (misal: "Kenapa pakai Custom User?", "Bagaimana cara debug email?", "Apa bedanya dev.py dan production.py?").

**Dependencies**: US-001

**Definition of Done**:
- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## Ringkasan

| ID | Judul | Prioritas | Estimasi |
|---|---|---|---|
| US-001 | Clone & jalankan project baru | Must | 2 |
| US-002 | Konfigurasi environment via `.env` | Must | 2 |
| US-003 | Custom User model siap pakai | Must | 2 |
| US-004 | Register akun baru | Must | 3 |
| US-005 | Login | Must | 2 |
| US-006 | Logout | Must | 1 |
| US-007 | Lupa password & reset | Must | 3 |
| US-008 | Verifikasi email | Must | 3 |
| US-009 | Edit profil & avatar | Must | 3 |
| US-010 | Layout dasar (navbar, sidebar, dashboard) | Must | 5 |
| US-011 | Komponen UI dasar | Must | 5 |
| US-012 | Admin Django kustom | Should | 3 |
| US-013 | Static & media files | Must | 2 |
| US-014 | Logging terstruktur | Should | 2 |
| US-015 | Error pages kustom (403, 404, 500) | Must | 2 |
| US-016 | Security headers production-ready | Must | 2 |
| US-017 | Test suite siap pakai | Must | 3 |
| US-018 | CI/CD GitHub Actions | Must | 3 |
| US-019 | CLAUDE.md untuk AI assistant | Should | 1 |
| US-020 | Authorization (Permission & Group) | Must | 3 |
| US-021 | Cache (Redis / Local Memory) | Must | 2 |
| US-022 | Email (SMTP / Console / Mailpit) | Must | 2 |
| US-023 | Dokumentasi project | Should | 3 |
| | **Total** | | **59 poin** |
