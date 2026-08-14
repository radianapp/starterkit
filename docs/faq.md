# FAQ

**Q: Mengapa komponen form terlihat berantakan di browser lama?**
A: RDP UI menggunakan CSS modern (seperti CSS Variables dan Flexbox/Grid). Pastikan Anda menggunakan browser versi terbaru.

**Q: Bagaimana cara menangani pesan error pada form?**
A: Setiap komponen form (seperti `<c-rdp.form.input>`) memiliki properti `error=""`. Cukup passing string pesan error dari backend, maka form akan otomatis berubah menjadi state *invalid* (garis merah) dan menampilkan pesan error di bawahnya.

**Q: Teks konten menghilang saat beralih antara Tema Gelap dan Terang?**
A: Masalah ini terjadi jika Anda hanya memanipulasi `data-theme` (milik PicoCSS) tanpa ikut memanipulasi `data-rdp-theme` dan me-refresh file CSS theme (`rdp-theme-css`). Gunakan fungsi `applyTheme()` dalam `layout-state.js` yang secara dinamis mengatur `<link>` stylesheet yang aktif berdasarkan teman yang sedang aktif, sehingga memastikan warna font (`--rdp-text`) sesuai dengan warna latar.

**Q: Mengapa menu Hamburger tidak muncul pada mode Tablet (lebar >768px)?**
A: Perilaku ini memang didesain demikian. Sesuai panduan *Responsive Strategy*, pada mode Tablet, sidebar dipadatkan menjadi *Icon Rail* dengan ukuran `224px` atau `64px`, yang berarti Navigasi Sidebar tidak sepenuhnya tersembunyi. Menu Hamburger HANYA akan muncul pada mode Mobile (`< 768px`) di mana seluruh Sidebar dipindah ke dalam *drawer/off-canvas*.

**Q: Apa perbedaan `FRAMEWORK_VERSION` dan `LOCAL_APP_VERSION`?**
A: `FRAMEWORK_VERSION` adalah versi *template sumber* RDP Starter Kit yang Anda clone dari GitHub — nilainya mencerminkan versi starter kit yang dijadikan fondasi. `LOCAL_APP_VERSION` adalah versi *aplikasi Anda sendiri* yang bisa Anda naikkan setiap kali melakukan rilis baru ke production. Keduanya dikonfigurasi via file `.env`.

**Q: Halaman Changelog kosong, bagaimana mengisinya?**
A: Halaman Changelog mengambil data dari database (model `SystemUpdate`). Tambahkan entri melalui **Admin Panel → Dashboard → System Updates → + Add**. Isi field `version`, `title`, `description`, dan `update_type`, lalu simpan. Entri akan langsung muncul di `/changelog/`.

**Q: Apakah nilai versi akan otomatis berubah saat framework diupdate dari GitHub?**
A: Tidak secara otomatis. Anda perlu memperbarui nilai `FRAMEWORK_VERSION` di file `.env` secara manual setelah melakukan `git pull` dari repository sumber. Ini adalah keputusan desain untuk menjaga transparansi dan kontrol penuh di tangan developer.

**Q: Apa yang terjadi jika file CSV untuk bulk upload memiliki lebih dari 1000 baris?**
A: Sistem secara otomatis akan mendelegasikan proses import ke Celery (background task). Admin akan mendapatkan pesan notifikasi hijau bahwa import akan diproses di background.

**Q: Mengapa user hasil bulk upload langsung di-redirect ke halaman "Ganti Password"?**
A: Ini adalah fitur keamanan dari `ForceChangePasswordMiddleware`. Pengguna baru wajib mengganti password default (yang dibuat acak oleh sistem) agar akun mereka lebih aman.

**Q: Apakah semua kolom tambahan (misalnya departemen atau jabatan) dari CSV akan disimpan?**
A: Ya. Semua kolom yang tidak standar pada `User` akan disimpan secara otomatis ke dalam kolom JSON `extra_data` di profil pengguna.

**Q: Mengapa AI/LLM lain kadang menilai proyek ini memiliki banyak sintaks/tag yang rusak?**
A: Banyak LLM hanya dilatih pada Django klasik dengan sintaks `{% block %}` dan berasumsi bahwa tag seperti `<c-rdp.button>` atau `<c-layout.base>` adalah tag HTML yang tidak valid. RDP Starter Kit menggunakan `django-cotton` sebagai framework komponen modern, di mana tag `<c-...>` dikompilasi secara otomatis oleh engine Cotton.

**Q: Mengapa pengujian form HTMX menghasilkan status HTTP 422? Apakah itu bug?**
A: Bukan. Mengembalikan status HTTP 422 (Unprocessable Entity) saat terjadi kegagalan validasi form adalah standar arsitektur HTMX. Status ini memberitahu HTMX agar menukar potongan HTML pesan error tanpa melakukan reload halaman penuh.

**Q: Bagaimana cara termudah menginstal project ini sebagai service di server Linux VPS?**
A: Anda cukup menjalankan skrip `./scripts/install_service.sh` atau via menu `./bin/deploy.sh` (pilih Opsi 6). Skrip akan otomatis mengonfigurasi Gunicorn systemd service, Nginx reverse proxy, dan SSL gratis dari Let's Encrypt / Certbot.

**Q: Bagaimana cara memperbarui kode di server production tanpa repot?**
A: Gunakan skrip `./scripts/deploy_prod.sh <nama_service>` atau via menu `./bin/deploy.sh` (pilih Opsi 7). Skrip ini otomatis menjalankan `git pull`, `uv sync --no-dev`, `python manage.py migrate`, `collectstatic`, dan me-restart Gunicorn daemon.

**Q: Apakah sertifikat SSL Let's Encrypt akan otomatis diperpanjang (auto-renew)?**
A: Ya. Certbot secara otomatis mendaftarkan timer systemd (`certbot.timer`) saat instalasi yang memeriksa dan memperpanjang masa berlaku sertifikat SSL setiap 60 hari.

**Q: Apakah Docker Compose standar dan layak untuk digunakan di server Production?**
A: **Ya, sangat standar dan banyak digunakan di industri** untuk deployment skala single-server/VPS. Docker Compose di production memberikan keunggulan isolasi proses, konsistensi lingkungan (dev ↔ prod), dan kemudahan migrasi server. Namun, pastikan menggunakan konfigurasi khusus production (`docker-compose.prod.yml`) yang menggunakan image immutable (bukan bind-mount source code), WSGI server (Gunicorn), `DEBUG=False`, restart policy (`restart: unless-stopped`), dan reverse proxy Nginx untuk melayani static/media files.

**Q: Apakah aplikasi Django Monolith bisa dideploy ke Kubernetes (K8s)? Bagaimana dengan databasenya?**
A: **Bisa 100% dan sangat lazim.** Perusahaan raksasa seperti Instagram dan Sentry menjalankan Django monolith di Kubernetes. Caranya adalah memecah proses dari image yang sama menjadi Pod Web (stateless autoscaling) dan Pod Celery Worker/Beat. Database PostgreSQL dan media uploads (S3) **wajib berada di luar Pod (Managed Services)** agar data tidak hilang saat Pod berganti node. Migrasi dijalankan sekali per deployment menggunakan Kubernetes `Job`.

**Q: Bagaimana RDP CLI mengenali bahwa suatu project adalah project RDP? Apakah bisa digunakan pada project Django lama (existing)?**
A: RDP CLI menggunakan sistem signature bertingkat: pertama membaca file manifest `rdp.json`, kedua memeriksa `[tool.rdp]` di `pyproject.toml`, dan ketiga fallback ke struktur folder `apps/` & `config/version.json` (untuk proyek versi lama). Perintah pintasan dasar (`rdp runserver`, `rdp migrate`, `rdp shell`) dapat berjalan di project Django standar mana pun. Namun, perintah generator (`rdp new app`, `rdp new crud`, `rdp make`) mengasumsikan konvensi RDP (struktur package per fungsi dan pustaka `django-cotton`).

**Q: Mengapa proyek RDP menggunakan file signature `rdp.json` daripada sekadar menebak struktur folder?**
A: Menggunakan file signature `rdp.json` (mirip `angular.json` atau `next.config.js`) memberikan kepastian deterministik tanpa menebak struktur, menyimpan versi skema framework yang digunakan, memungkinkan kustomisasi path (`apps_dir`, `settings_file`), dan tetap menjaga kompatibilitas mundur (*backward compatibility*) penuh dengan proyek RDP versi terdahulu melalui mekanisme fallback otomatis.






