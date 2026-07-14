# FAQ

**Q: Mengapa komponen form terlihat berantakan di browser lama?**
A: RDP UI menggunakan CSS modern (seperti CSS Variables dan Flexbox/Grid). Pastikan Anda menggunakan browser versi terbaru.

**Q: Bagaimana cara menangani pesan error pada form?**
A: Setiap komponen form (seperti `<c-rdp.form.input>`) memiliki properti `error=""`. Cukup passing string pesan error dari backend, maka form akan otomatis berubah menjadi state *invalid* (garis merah) dan menampilkan pesan error di bawahnya.

**Q: Teks konten menghilang saat beralih antara Tema Gelap dan Terang?**
A: Masalah ini terjadi jika Anda hanya memanipulasi `data-theme` (milik PicoCSS) tanpa ikut memanipulasi `data-rdp-theme` dan me-refresh file CSS theme (`rdp-theme-css`). Gunakan fungsi `applyTheme()` dalam `layout-state.js` yang secara dinamis mengatur `<link>` stylesheet yang aktif berdasarkan teman yang sedang aktif, sehingga memastikan warna font (`--rdp-text`) sesuai dengan warna latar.

**Q: Mengapa menu Hamburger tidak muncul pada mode Tablet (lebar >768px)?**
A: Perilaku ini memang didesain demikian. Sesuai panduan *Responsive Strategy*, pada mode Tablet, sidebar dipadatkan menjadi *Icon Rail* dengan ukuran `224px` atau `64px`, yang berarti Navigasi Sidebar tidak sepenuhnya tersembunyi. Menu Hamburger HANYA akan muncul pada mode Mobile (`< 768px`) di mana seluruh Sidebar dipindah ke dalam *drawer/off-canvas*.
