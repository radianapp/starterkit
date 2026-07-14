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

## US-024: CLI `rdp new` — wizard interaktif bootstrap project

**Story**:
Sebagai developer, saya ingin menjalankan `uv run scripts/rdp_new.py myproject` dan menjawab beberapa pertanyaan singkat, sehingga project Django baru siap `runserver` dalam < 5 menit tanpa edit manual.

**Prioritas**: Should
**Estimasi**: 5
**FR**: FR-01, FR-02

**Acceptance Criteria**:

- Given `uv run scripts/rdp_new.py myproject` dijalankan, When wizard berjalan, Then menanyakan: nama project (pre-fill "myproject"), deskripsi singkat, app color (pilihan: teal/coral/purple/amber/gold/navy), dan halaman opsional (contact, FAQ).
- Given wizard selesai, When script selesai, Then folder `myproject/` berisi project lengkap: SECRET_KEY unik di `.env`, semua referensi nama project sudah di-rename, `--rdp-app-accent` di-set sesuai pilihan warna.
- Given project hasil wizard, When developer menjalankan `uv sync && uv run python manage.py migrate && uv run python manage.py runserver`, Then server berjalan tanpa error dan halaman landing tampil.
- Given jalur alternatif (clone manual FR-04), When developer mengikuti README tanpa CLI, Then project tetap berjalan — wizard tidak memblokir jalur lama.

**Dependencies**: US-001, US-002, US-027 (layout harus sudah ada agar project hasil wizard langsung tampil)

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-025: Template app untuk `manage.py startapp --template`

**Story**:
Sebagai developer, saya ingin menjalankan `uv run python manage.py startapp myapp --template=app_template` dan mendapatkan struktur package yang sudah benar, sehingga tidak perlu membuat folder `models/`, `views/`, `services/` secara manual setiap kali.

**Prioritas**: Should
**Estimasi**: 2
**FR**: FR-03

**Acceptance Criteria**:

- Given template app tersedia di `scripts/app_template/`, When developer menjalankan `startapp myapp --template=scripts/app_template`, Then folder `apps/myapp/` berisi: `models/`, `views/`, `services/`, `forms/`, `admin/`, `tests/`, masing-masing dengan `__init__.py` kosong dan `urls.py`.
- Given app baru dibuat, When developer membuka `models/__init__.py`, Then ada contoh import dan docstring format standar.
- Given app baru dibuat, When developer membuka `views/__init__.py`, Then ada contoh CBV dengan referensi US placeholder dan docstring format standar.
- Given `startapp` dijalankan, When hasilnya di-inspect, Then tidak ada file flat `models.py`, `views.py` (semua sudah package).

**Dependencies**: US-001

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-026: Self-host RDP-UI aset via env var

**Story**:
Sebagai developer yang deploy ke environment tanpa akses CDN, saya ingin mengaktifkan self-host mode dengan satu env var, sehingga semua aset RDP-UI/PicoCSS/HTMX dilayani dari `static/` lokal tanpa mengubah template.

**Prioritas**: Should
**Estimasi**: 2
**FR**: FR-06

**Acceptance Criteria**:

- Given `RDP_UI_SELF_HOST=False` (default), When halaman dirender, Then aset di-load dari CDN berversi (path: `cdn.radian.web.id/v{RDP_UI_VERSION}/assets/...`).
- Given `RDP_UI_SELF_HOST=True` di `.env`, When halaman dirender, Then URL aset berubah ke `{% static 'vendor/rdp-ui/...' %}` — tidak ada CDN request.
- Given mode self-host aktif, When `python manage.py collectstatic`, Then semua aset vendor tersedia di `staticfiles/`.
- Given `RDP_UI_VERSION=v1.0` di `.env`, When CDN mode aktif, Then URL aset mengandung `/v1.0/` — bukan path tanpa versi.

**Dependencies**: US-001, US-002, US-013

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-027: Layout system lengkap — 7 komponen Cotton sesuai konvensi v0.2

**Story**:
Sebagai developer, saya ingin tujuh layout Cotton (`<c-layout.base|auth|public|dashboard|error|email|print>`) tersedia dengan naming sesuai PRD v0.2 dan bebas inline CSS, sehingga setiap jenis halaman punya shell yang tepat tanpa menulis HTML dari nol.

**Prioritas**: Must
**Estimasi**: 3
**FR**: FR-05, FR-07

**Acceptance Criteria**:

- Given `<c-layout.base>`, When dirender, Then load order: PicoCSS → `rdp.css` (berversi) → HTMX → `rdp.js` → Alpine.js; ada skip-nav link; `data-theme` ada di `<html>`; CSRF meta tag ada; `debug.css` hanya diload jika `RDP_DEBUG_OVERLAY` aktif.
- Given `<c-layout.auth>`, When dipakai di halaman login/register, Then tampil layout terpusat (centered content) tanpa navbar/sidebar.
- Given `<c-layout.public>`, When dipakai di halaman landing/about, Then tampil navbar publik + footer; mendukung slot `nav_links`.
- Given `<c-layout.dashboard>`, When dipakai di halaman app, Then tampil topbar + sidebar + main content + footer.
- Given `<c-layout.error>`, When dipakai di 403/404/500, Then tampil layout sederhana terpusat tanpa sidebar.
- Given `<c-layout.email>`, When dipakai di template email HTML, Then output HTML dengan CSS inline-safe (tanpa link CDN eksternal) dan layout yang konsisten di email client.
- Given `<c-layout.print>`, When dipakai dan halaman di-print, Then sidebar/navbar tersembunyi, konten utama penuh lebar.
- Given **semua layout**, When di-inspect, Then tidak ada atribut `style="..."` inline.

**Dependencies**: US-010, US-026

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-028: App shell lengkap — persistent theme, toast global, modal global

**Story**:
Sebagai developer, saya ingin `<c-layout.dashboard>` sudah menyediakan tema persisten, container toast global, dan container modal global, sehingga semua halaman app langsung mendapat fitur ini tanpa setup per-halaman.

**Prioritas**: Must
**Estimasi**: 3
**FR**: FR-08

**Acceptance Criteria**:

- Given user toggle dark/light mode via theme switcher di topbar, When halaman di-refresh, Then tema tersimpan (localStorage key `rdp-theme`) dan halaman langsung tampil dengan tema yang sama.
- Given HTMX trigger `HX-Trigger: {"showToast": {"message": "Berhasil!", "type": "success"}}` di-return dari server, When response diterima, Then toast muncul di container global (pojok kanan bawah), auto-dismiss setelah 4 detik.
- Given HTMX response dengan header `HX-Trigger: {"openModal": {"url": "/partial/form/"}}`, When response diterima, Then modal global terbuka dan load konten dari URL tersebut.
- Given viewport 375px, When sidebar toggle diklik, Then sidebar menjadi drawer overlay di atas konten; klik di luar drawer menutupnya.
- Given topbar, When dirender, Then ada slot `topbar_actions` untuk menambah tombol custom per halaman.

**Dependencies**: US-027

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-029: HTMX form validation pattern — 422 fragment + HX-Redirect

**Story**:
Sebagai developer, saya ingin ada mixin/helper standar untuk form HTMX yang mengembalikan fragment 422 saat error dan HX-Redirect saat sukses, sehingga semua form di project konsisten dan tidak perlu menulis logika yang sama berulang.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-10

**Acceptance Criteria**:

- Given `HtmxFormMixin` di `apps/core/mixins/`, When form valid dan request dari HTMX, Then view mengembalikan response dengan header `HX-Redirect: /target/url/`.
- Given `HtmxFormMixin`, When form invalid dan request dari HTMX, Then view mengembalikan HTTP 422 berisi fragment HTML form dengan error per field.
- Given form yang menggunakan mixin, When request bukan HTMX (misalnya direct URL), Then fallback ke perilaku form Django biasa (redirect atau re-render dengan error).
- Given contoh implementasi di `apps/core/`, When developer membacanya, Then bisa langsung copy-paste pattern ke view baru.

**Dependencies**: US-001, US-010

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-030: Layout email + template email transaksional

**Story**:
Sebagai developer, saya ingin `<c-layout.email>` dan template email verifikasi/reset password sudah tersedia, sehingga email transaksional konsisten dengan brand RDP tanpa menulis HTML email dari nol.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-11

**Acceptance Criteria**:

- Given `<c-layout.email>`, When dipakai di template email, Then output HTML menggunakan inline CSS (kompatibel Gmail/Outlook), ada slot `subject`, `header`, default content, `footer`.
- Given template email verifikasi (`templates/email/verify_email.html`), When di-preview di Mailpit, Then tampil layout branded dengan link verifikasi yang benar dan tombol CTA.
- Given template email reset password (`templates/email/password_reset.html`), When di-preview, Then tampil link reset dengan informasi expiry.
- Given kedua template, When di-render, Then tidak ada CDN external link (semua styling inline).

**Dependencies**: US-022, US-027

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-031: Public pages — landing, about, terms, privacy

**Story**:
Sebagai developer yang baru clone starter kit, saya ingin halaman publik (landing, about, terms, privacy) sudah tersedia dengan konten placeholder terstruktur, sehingga saya bisa langsung replace konten tanpa membangun layout dari nol.

**Prioritas**: Must
**Estimasi**: 3
**FR**: FR-12

**Acceptance Criteria**:

- Given `http://localhost:8000/`, When dibuka tanpa login, Then tampil landing page menggunakan `<c-layout.public>` dengan section: hero (headline + CTA), grid fitur (3 kolom), footer.
- Given `http://localhost:8000/about/`, When dibuka, Then tampil halaman about dengan placeholder konten terstruktur (nama perusahaan, deskripsi, nilai-nilai).
- Given `http://localhost:8000/terms/` dan `/privacy/`, When dibuka, Then tampil halaman dengan konten placeholder terstruktur (section-section umum terms/privacy).
- Given semua halaman public, When di-inspect, Then menggunakan `<c-layout.public>` dan komponen `<c-rdp.*>` — tidak ada HTML mentah berulang.
- Given wizard CLI memilih contact/FAQ, When project di-generate, Then `http://localhost:8000/contact/` dan `/faq/` juga tersedia.

**Dependencies**: US-027

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-032: Dashboard default dengan demo data — KPI cards, tabel, pagination

**Story**:
Sebagai developer yang baru login ke project hasil starter kit, saya ingin dashboard menampilkan KPI cards, tabel data dengan pagination, dan area chart placeholder yang terisi demo data, sehingga dashboard tidak pernah tampil kosong dan langsung terlihat fungsional.

**Prioritas**: Must
**Estimasi**: 3
**FR**: FR-13

**Acceptance Criteria**:

- Given developer baru login setelah `loaddata demo_data.json`, When membuka `/dashboard/`, Then tampil: ≥ 4 KPI/stat cards dengan angka dari DB, tabel dengan ≥ 5 baris data, dan area chart placeholder.
- Given tabel di dashboard, When data > 10 baris, Then pagination muncul dan berfungsi via HTMX fragment (bukan full reload).
- Given stat cards, When angka berubah (mis. user baru register), Then data di dashboard mencerminkan data real dari DB — bukan hardcoded di template.
- Given `uv run python manage.py loaddemodata`, When dijalankan, Then demo data ter-load ke DB tanpa error; idempotent (aman dijalankan ulang).

**Dependencies**: US-005, US-027, US-028, US-037

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-033: Komponen Cotton RDP-UI v1.0 gap — badge, avatar, loader

**Story**:
Sebagai developer, saya ingin `<c-rdp.badge>`, `<c-rdp.avatar>`, dan `<c-rdp.loader>` tersedia sebagai komponen Cotton dengan props terdokumentasi, sehingga tidak perlu menulis class RDP-UI secara manual setiap kali.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-15

**Acceptance Criteria**:

- Given `<c-rdp.badge variant="success">Selesai</c-rdp.badge>`, When dirender, Then tampil badge dengan warna sukses sesuai RDP-UI dan mendukung `variant`: success/warning/danger/info/neutral.
- Given `<c-rdp.avatar name="Rahadi" src="/media/avatar.jpg" size="md">`, When dirender, Then tampil avatar dengan gambar jika `src` ada; fallback ke inisial nama jika tidak ada.
- Given `<c-rdp.loader>`, When dirender, Then tampil AI loader spinner sesuai komponen RDP-UI.
- Given semua komponen baru, When atribut tidak dikenal di-pass, Then di-forward ke elemen HTML dasar via `{{ attrs }}`.

**Dependencies**: US-011

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-034: Component library gap — tabs, toast, tooltip, accordion, skeleton, empty state, stat card, progress, drawer, search box, filter bar, file upload, steps

**Story**:
Sebagai developer, saya ingin komponen-komponen yang belum ada di RDP-UI v1.0 tersedia sebagai Cotton + CSS lokal (`static/css/components/`), sehingga saya tidak perlu mengarang komponen yang sama di tiap project.

**Prioritas**: Must
**Estimasi**: 8
**FR**: FR-16, FR-17

**Acceptance Criteria**:

- Given `<c-rdp.tabs>`, When dirender dengan beberapa tab item, Then tab switching berfungsi via Alpine.js; active tab tersimpan di URL hash opsional.
- Given `<c-rdp.toast message="Berhasil!" type="success">`, When dirender, Then toast tampil dan auto-dismiss setelah 4 detik; mendukung type: success/warning/danger/info.
- Given `<c-rdp.tooltip content="Keterangan">`, When elemen di-hover, Then tooltip muncul di atas elemen.
- Given `<c-rdp.accordion>`, When header diklik, Then panel expand/collapse dengan animasi.
- Given `<c-rdp.skeleton width="100%" height="20px">`, When dirender, Then tampil loading skeleton placeholder.
- Given `<c-rdp.empty-state icon="📭" title="Belum ada data">`, When dirender, Then tampil empty state dengan ikon, judul, deskripsi opsional, dan slot action.
- Given `<c-rdp.stat-card label="Total User" value="142" trend="+12%" trend_up="true">`, When dirender, Then tampil stat card dengan label, nilai besar, dan indikator trend.
- Given `<c-rdp.confirm title="Hapus item?" destructive="true">`, When trigger diklik, Then dialog konfirmasi muncul dengan tombol Batal dan Lanjutkan (merah); terintegrasi dengan HTMX delete pattern.
- Given `<c-rdp.progress value="75" max="100">`, When dirender, Then tampil progress bar 75%.
- Given `<c-rdp.drawer>`, When trigger diklik, Then drawer slide-in dari kanan; Esc dan klik di luar menutupnya.
- Given `<c-rdp.search-box placeholder="Cari...">`, When dirender, Then input search dengan debounce HTMX 300ms.
- Given `<c-rdp.file-upload accept="image/*" max_size="2MB">`, When file dipilih, Then validasi ukuran dan tipe di client-side sebelum upload.
- Given `<c-rdp.steps current="2">`, When dirender dengan 3 step items, Then tampil wizard indicator dengan step aktif yang jelas.
- Given **semua komponen gap**, When CSS-nya di-inspect, Then menggunakan token `var(--rdp-*)` dan class `rdp-*` — tidak ada warna hex hardcoded.

**Dependencies**: US-011, US-028

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-035: Halaman demo komponen internal `/dev/components/`

**Story**:
Sebagai developer, saya ingin membuka `/dev/components/` dan melihat semua varian komponen Cotton yang tersedia, sehingga saya punya referensi visual langsung tanpa membuka dokumentasi eksternal — dan halaman ini tidak pernah ter-expose di production.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-18

**Acceptance Criteria**:

- Given `DEBUG=True`, When developer membuka `/dev/components/`, Then tampil halaman yang menampilkan semua varian setiap komponen: button (semua variant+size), badge, alert, card, modal, table, pagination, tabs, toast, tooltip, accordion, skeleton, empty state, stat card, confirm dialog, progress, drawer, search box, file upload, steps.
- Given `DEBUG=False` (production), When request ke `/dev/components/` masuk, Then response 404 — URL tidak terdaftar.
- Given halaman `/dev/components/`, When dibuka, Then menggunakan `<c-layout.dashboard>` dan setiap komponen diberi label nama + contoh kode snippet (sebagai `<code>` block).

**Dependencies**: US-027, US-033, US-034

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-036: 10 HTMX patterns — contoh hidup + resep cookbook

**Story**:
Sebagai developer, saya ingin minimal 10 pattern HTMX terimplementasi sebagai halaman/endpoint contoh di project dan terdokumentasi sebagai resep cookbook, sehingga saya (dan AI assistant) tinggal mengikuti pattern yang sudah ada.

**Prioritas**: Must
**Estimasi**: 5
**FR**: FR-19

**Acceptance Criteria**:

- Given project starter kit, When developer membuka source code, Then tersedia contoh hidup (template + view + URL) untuk semua pattern berikut: CRUD list + form, modal form, delete confirmation, live validation field, inline edit, search dengan debounce, pagination fragment, infinite scroll, polling status, toast via `HX-Trigger`.
- Given setiap pattern, When request dikirim dari HTMX, Then konvensi response dipatuhi: error form = HTTP 422 + fragment, sukses full-page = `HX-Redirect`, toast = `HX-Trigger: {"showToast": {...}}`.
- Given contoh di project, When developer membuka `docs/cookbook/htmx-patterns.md`, Then setiap pattern punya: deskripsi singkat, kode template (HTMX attributes), kode view (Django), dan konvensi response — cukup copy-paste untuk mulai.

**Dependencies**: US-029, US-028, US-034

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-037: Management command demo data

**Story**:
Sebagai developer yang baru clone starter kit, saya ingin menjalankan satu perintah untuk membuat sample user dan data contoh, sehingga dashboard tidak tampil kosong dan semua fitur bisa langsung dicoba tanpa input manual.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-20

**Acceptance Criteria**:

- Given project baru di-setup, When developer menjalankan `uv run python manage.py loaddemodata`, Then terbuat: 1 superuser (admin@rdp.test/admin123), 2 regular user, dan data contoh untuk semua model yang ada di dashboard.
- Given perintah dijalankan ulang, When data sudah ada, Then perintah idempotent — tidak error, tidak duplikasi data (gunakan `get_or_create`).
- Given demo data, When developer login sebagai user biasa, Then dashboard menampilkan data yang relevan dan tidak tampil kosong.
- Given perintah, When dijalankan, Then print summary: berapa user dibuat, berapa record data contoh dibuat.

**Dependencies**: US-005, US-032

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-038: Script lint template + integrasi CI

**Story**:
Sebagai developer, saya ingin CI otomatis gagal jika ada inline `style=`, blok `<script>` inline, atau warna hex hardcoded di template/CSS, sehingga pelanggaran SOP frontend terdeteksi sebelum masuk ke main branch.

**Prioritas**: Must
**Estimasi**: 3
**FR**: FR-21

**Acceptance Criteria**:

- Given `uv run python scripts/lint_templates.py`, When dijalankan di root project, Then script mendeteksi dan melaporkan (file:line): atribut `style="..."` di template HTML, blok `<script>` inline di template (whitelist: script dengan `type="application/ld+json"`), dan nilai warna hex (`#[0-9a-fA-F]{3,6}`) di file CSS project (bukan vendor).
- Given template yang bersih, When script dijalankan, Then exit code 0 (tidak ada error).
- Given template dengan pelanggaran, When script dijalankan, Then exit code 1 dengan output daftar pelanggaran.
- Given GitHub Actions workflow, When developer push code dengan pelanggaran, Then CI gagal di step "Lint templates" sebelum step test.

**Dependencies**: US-018 (CI GitHub Actions)

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-039: Restrukturisasi `docs/` sesuai standar v0.2

**Story**:
Sebagai developer (dan AI assistant), saya ingin folder `docs/` terstruktur dengan subfolder yang jelas (`prd/`, `sop/`, `cookbook/`, `modules/`, `architecture/`, `decisions/`), sehingga mudah menemukan dokumen yang relevan tanpa tebak-tebakan.

**Prioritas**: Must
**Estimasi**: 2
**FR**: FR-23

**Acceptance Criteria**:

- Given repo setelah story ini selesai, When developer membuka `docs/`, Then ada subfolder: `prd/` (PRD aktif + arsip), `prd/user-stories/`, `architecture/`, `decisions/`, `modules/`, `cookbook/`, `sop/`.
- Given file existing yang dipindah, When developer mengikuti link di CLAUDE.md, README, atau skill files, Then link tidak 404 — semua referensi sudah diupdate.
- Given `docs/PRDv0.1.md`, When dipindah, Then ada di `docs/prd/archive/PRDv0.1.md`.
- Given `docs/SOP-FRONTEND-STRUCTURE.md`, When dipindah, Then ada di `docs/sop/frontend-structure.md`.
- Given `docs/user-stories/rdp-starter-kit.md`, When dipindah, Then ada di `docs/prd/user-stories/rdp-starter-kit.md`.

**Dependencies**: —

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-040: SOP lengkap — HTMX, Cotton, Git, testing, modul

**Story**:
Sebagai developer baru di project RDP, saya ingin ada dokumen SOP untuk setiap aspek development utama, sehingga saya (dan AI assistant) bisa mengikuti standar yang sudah ada tanpa bertanya.

**Prioritas**: Should
**Estimasi**: 3
**FR**: FR-24

**Acceptance Criteria**:

- Given `docs/sop/`, When developer membukanya, Then ada file SOP untuk: frontend structure (sudah ada — dipindah dari US-039), HTMX patterns (konvensi response: 422/HX-Redirect/HX-Trigger), Cotton component (naming/props/slot/`{{ attrs }}`), Git workflow (branch/commit message/release), testing (unit/integration/setup pytest), dokumentasi modul.
- Given setiap SOP, When dibaca, Then berisi contoh kode konkret yang bisa langsung ditiru — bukan hanya deskripsi abstrak.
- Given SOP HTMX, When developer membacanya, Then pembagian tanggung jawab antara HTMX/rdp.js/Alpine.js jelas: HTMX = server round-trip, rdp.js = perilaku komponen RDP, Alpine = state UI lokal sisa.
- Given CLAUDE.md, When dibaca, Then ada referensi eksplisit ke semua SOP di `docs/sop/`.

**Dependencies**: US-036, US-039

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-041: Cookbook resep langkah-demi-langkah

**Story**:
Sebagai developer, saya ingin `docs/cookbook/` berisi resep langkah-demi-langkah untuk tugas-tugas umum, sehingga tidak perlu mencari referensi di luar project.

**Prioritas**: Should
**Estimasi**: 3
**FR**: FR-25

**Acceptance Criteria**:

- Given `docs/cookbook/`, When developer membukanya, Then ada resep untuk: buat CRUD baru (model + views + URLs + template), buat modal HTMX, buat wizard multi-step, tambah Django app baru, ganti app color, aktifkan Celery, aktifkan ASGI, aktifkan DRF, aktifkan S3.
- Given resep CRUD, When developer mengikutinya langkah per langkah, Then fitur CRUD berfungsi di akhir tanpa lookup tambahan.
- Given resep "tambah app baru", When developer mengikutinya, Then hasilnya konsisten dengan struktur package yang berlaku (menggunakan `startapp --template` dari US-025).
- Given resep "aktifkan Celery", When developer mengikutinya, Then ada task contoh yang berjalan dan bisa di-test secara lokal.

**Dependencies**: US-036, US-039, US-025

**Definition of Done**:

- [ ] Kode + unit test
- [ ] Acceptance criteria lolos manual test
- [ ] Dokumentasi modul diperbarui (docs/modules/)

---

## US-042: Workflow update skills AI seiring perubahan konvensi

**Story**:
Sebagai developer yang mengubah konvensi atau menambah pattern baru di starter kit, saya ingin ada panduan eksplisit dan checklist commit untuk memastikan skills AI di `.claude/` selalu up-to-date, sehingga AI assistant tidak menyarankan pattern yang sudah outdated.

**Prioritas**: Should
**Estimasi**: 1
**FR**: FR-26

**Acceptance Criteria**:

- Given developer mengubah konvensi (misalnya cara penulisan Cotton slot, atau pattern HTMX baru), When commit dibuat, Then commit message mencantumkan `[skills-updated]` dan file skill yang diupdate masuk dalam diff commit yang sama.
- Given CLAUDE.md, When dibaca, Then ada instruksi eksplisit: "setiap perubahan konvensi wajib update skill terkait di `.claude/` dalam commit yang sama".
- Given checklist PR/commit di `docs/sop/git-workflow.md`, When developer membuka checklist, Then ada item: "[ ] Jika mengubah konvensi/pattern — update `.claude/skills/` skill terkait".

**Dependencies**: US-039, US-040

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
| US-024 | CLI `rdp new` — wizard interaktif bootstrap project | Should | 5 |
| US-025 | Template app untuk `manage.py startapp --template` | Should | 2 |
| US-026 | Self-host RDP-UI aset via env var | Should | 2 |
| US-027 | Layout system lengkap — 7 komponen Cotton sesuai konvensi v0.2 | Must | 3 |
| US-028 | App shell lengkap — persistent theme, toast global, modal global | Must | 3 |
| US-029 | HTMX form validation pattern — 422 fragment + HX-Redirect | Must | 2 |
| US-030 | Layout email + template email transaksional | Must | 2 |
| US-031 | Public pages — landing, about, terms, privacy | Must | 3 |
| US-032 | Dashboard default dengan demo data — KPI cards, tabel, pagination | Must | 3 |
| US-033 | Komponen Cotton RDP-UI v1.0 gap — badge, avatar, loader | Must | 2 |
| US-034 | Component library gap — tabs, toast, tooltip, accordion, skeleton, dst. | Must | 8 |
| US-035 | Halaman demo komponen internal `/dev/components/` | Must | 2 |
| US-036 | 10 HTMX patterns — contoh hidup + resep cookbook | Must | 5 |
| US-037 | Management command demo data | Must | 2 |
| US-038 | Script lint template + integrasi CI | Must | 3 |
| US-039 | Restrukturisasi `docs/` sesuai standar v0.2 | Must | 2 |
| US-040 | SOP lengkap — HTMX, Cotton, Git, testing, modul | Should | 3 |
| US-041 | Cookbook resep langkah-demi-langkah | Should | 3 |
| US-042 | Workflow update skills AI seiring perubahan konvensi | Should | 1 |
| | **Total** | | **116 poin** |
