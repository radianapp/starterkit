# Solusi Enterprise: Pagination untuk Jutaan Baris Data (Big Data)

Dokumen ini menjelaskan strategi tingkat lanjut untuk menangani fitur *Paging/Pagination* pada tabel yang memiliki jutaan baris (jutaan *records*) dalam kerangka kerja **RDP (Django + HTMX + PostgreSQL)**.

---

## 1. Masalah pada Paginator Bawaan Django

Secara bawaan, kelas `django.core.paginator.Paginator` dirancang untuk membagi data dan memberikan informasi secara presisi, seperti:
`"Menampilkan halaman 2 dari 50.000 (Total Data: 1.000.000)"`

Untuk dapat menampilkan teks tersebut, `Paginator` di belakang layar akan menjalankan *query*:
```sql
SELECT COUNT(*) FROM nama_tabel WHERE kondisi...;
```

Pada *database* relasional seperti PostgreSQL, mengeksekusi `COUNT(*)` pada tabel raksasa sangat lambat karena harus memindai (scan) setiap baris secara fisik untuk memastikan data mana yang masih ada (terkait *Multiversion Concurrency Control* / MVCC). Akibatnya, meskipun aplikasi Anda hanya butuh 20 baris, server tetap tersendat (misal: jeda 1-3 detik) hanya untuk menghitung total keseluruhan data.

Namun, di sisi antarmuka pengguna (HTMX), masalah ini **TIDAK ADA**. HTMX tetap ringan dan super-cepat karena ia tidak perlu memuat JSON raksasa. Masalah hanya bersumber pada fungsi `COUNT(*)` dari Django.

---

## 2. Strategi Tingkat Lanjut (Backend)

Ketika aplikasi mulai melambat di halaman daftar produk atau log karena datanya terlalu besar, Anda **TIDAK PERLU** merombak arsitektur HTMX. Anda hanya perlu mengganti kelas/logic `Paginator` di *Views* dengan salah satu dari tiga solusi di bawah ini:

### A. Nonaktifkan `COUNT(*)` (Paginator Estimasi)

Jika aplikasi tidak mewajibkan angka total data yang *exact* (pasti), kita dapat menggunakan **Estimasi Baris Bawaan PostgreSQL**. 
Alih-alih `SELECT COUNT(*)`, PostgreSQL menyimpan perkiraan kasar jumlah baris di tabel sistemnya (yang dapat diambil dalam waktu kurang dari 1 milidetik).

**Cara Implementasi:**
Buat kelas *Paginator* khusus yang membajak metode `count`.
```python
from django.core.paginator import Paginator
from django.db import connection

class LargeTablePaginator(Paginator):
    """
    Paginator khusus yang mem-bypass query COUNT(*) lambat 
    dan mengambil estimasi baris dari PostgreSQL.
    """
    @property
    def count(self):
        if hasattr(self, '_count'):
            return self._count
            
        # Jika ada filter kompleks (q=...), fallback ke count biasa
        # Jika hanya query tabel utuh, gunakan reltuples PostgreSQL
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT reltuples FROM pg_class WHERE relname = %s",
                    [self.object_list.query.model._meta.db_table]
                )
                self._count = int(cursor.fetchone()[0])
        except Exception:
            self._count = super().count
            
        return self._count
```
*(Gunakan kelas ini sebagai pengganti `Paginator` bawaan di dalam `ListView`)*.

### B. Keyset / Cursor Pagination (Opsi Terbaik & Tercepat)

Ini adalah metode *Enterprise* (yang digunakan oleh Facebook, X/Twitter, dan Google). 
Alih-alih melompat dengan klausa `OFFSET` (misal: lompati 1 juta baris pertama lalu ambil 20), metode ini "mengingat" titik terakhir data yang dilihat.

**Contoh Query SQL:**
Alih-alih: `SELECT * FROM log ORDER BY id DESC LIMIT 20 OFFSET 50000;`
Menjadi: `SELECT * FROM log WHERE id < [ID_TERAKHIR_DILIHAT] ORDER BY id DESC LIMIT 20;`

**Cara Implementasi:**
Gunakan pustaka tambahan pihak ketiga (contoh: `django-cursor-pagination`) atau bangun kustom. 
**Catatan untuk UI:** Metode ini **tidak mendukung** fitur "Lompat langsung ke halaman 50". Pengguna hanya bisa menekan tombol "Berikutnya" atau "Sebelumnya", atau *Infinite Scroll*. Tombol `HTMX` Anda tinggal disesuaikan untuk mengirim parameter `?last_id=...` bukan lagi `?page=2`.

### C. Ganti UI menjadi "Load More" / "Infinite Scroll"

Jika tabel sudah menyentuh ratusan juta baris, maka pola UX (Pengalaman Pengguna) "Halaman 1, 2, 3..." biasanya tidak relevan lagi. Mengubah desain menjadi tombol `"Muat Lebih Banyak" (Load More)` menggunakan *HTMX* jauh lebih cepat.

- Tidak perlu ada hitungan *Total Data*.
- Cukup ambil batasan 20 baris plus 1 baris ekstra (`LIMIT 21`). 
- Jika *database* mengembalikan 21 baris, berarti masih ada data di halaman selanjutnya. Tampilkan 20, dan aktifkan tombol "Selanjutnya".

---

## 3. Ringkasan untuk Tim RDP

- **Data Skala Kecil–Menengah (< 100.000 baris):** Gunakan `ListView` + `paginate_by` bawaan Django seperti biasa (seperti halaman Daftar Produk saat ini). Kecepatan masih 100% optimal.
- **Data Skala Besar (Jutaan Baris):** Jika UX mulai lambat saat *paging*, Anda hanya perlu melakukan "tweak" `Paginator` di file *View* Django tanpa perlu menyentuh template HTML atau sistem HTMX.
