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
