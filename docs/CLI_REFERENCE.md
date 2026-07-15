# Referensi RDP CLI

RDP (Radian Data Platform) CLI adalah alat baris perintah (*command-line interface*) yang dirancang khusus untuk menyederhanakan pengembangan, pengelolaan komponen UI, dan pembaruan (*update*) pada proyek yang dibangun menggunakan RDP Framework.

## Daftar Perintah (Commands)

### 1. `rdp init <nama_proyek>`
Menginisialisasi proyek baru berdasarkan RDP Starterkit.
- **Deskripsi:** Perintah ini akan mengkloning/menyalin struktur *template base* RDP ke direktori lokal Anda, membersihkan riwayat `.git` asal dari framework, dan menyiapkan nama proyek Anda secara otomatis.
- **Penggunaan:** 
  ```bash
  rdp init aplikasi_keuangan
  ```

### 2. `rdp add <nama_komponen>`
Menyalin komponen UI Cotton secara modular dari repositori pusat RDP langsung ke dalam folder proyek Anda (tepatnya di `templates/cotton/`).
- **Deskripsi:** Memungkinkan Anda mengambil komponen hanya saat dibutuhkan (terinspirasi dari konsep Shadcn UI). Setelah disalin, komponen tersebut sepenuhnya menjadi "milik" proyek Anda (*Own Your Code*). Anda bebas memodifikasi HTML, logika, atau CSS komponen tersebut tanpa takut rusak.
- **Penggunaan:**
  ```bash
  rdp add modal
  rdp add datatable
  ```

### 3. `rdp update`
Memeriksa dan memperbarui file inti (*core engine*) atau komponen UI bawaan yang digunakan oleh proyek Anda.
- **Deskripsi:** Karena pendekatan RDP adalah *Own Your Code*, perintah ini **tidak akan langsung menimpa** kode lokal yang telah Anda modifikasi secara sepihak. Saat dijalankan, CLI akan menarik versi terbaru dan membandingkannya (*diff*) dengan file lokal:
  - **Sama / Belum Dimodifikasi:** Komponen akan otomatis diperbarui ke versi terbaru.
  - **Ada Modifikasi Lokal:** CLI akan mendeteksi perubahan Anda dan menampilkan peringatan interaktif, memberi opsi untuk: *Menimpa (Overwrite)*, *Melewati (Skip)*, atau *Menyatukan (Merge)* secara manual.
- **Penggunaan:**
  ```bash
  rdp update
  ```

### 4. `rdp serve`
Menjalankan *development server*.
- **Deskripsi:** Merupakan pintasan cepat (alias) yang pada dasarnya mengeksekusi server bawaan Django (`python manage.py runserver`), yang juga sudah mencakup *watcher* dasar atau terintegrasi dengan utilitas *hot-reload*.
- **Penggunaan:**
  ```bash
  rdp serve
  ```

### 5. `rdp make-component <nama_komponen>`
Membuat *skeleton* atau kerangka dasar untuk komponen Cotton yang baru.
- **Deskripsi:** Perintah ini akan secara otomatis membuat file `<nama_komponen>.html` baru di dalam direktori `templates/cotton/`, lengkap dengan pembungkus standar dan *tag* `<c-vars>` bawaan sehingga Anda bisa langsung mulai menyusun kode.
- **Penggunaan:**
  ```bash
  rdp make-component widget_chart
  ```

## Memperbarui (Update) Alat CLI RDP
Sistem CLI RDP (yakni alat `rdp` itu sendiri, bukan file proyek) adalah aplikasi terpisah yang terinstal secara global di sistem Anda (misalnya di `C:\Users\nama_user\.local\bin\rdp.exe`).

CLI ini memiliki fitur *self-updater* yang secara otomatis akan mengecek repositori GitHub untuk mencari rilis terbaru. Untuk memperbarui CLI Anda, cukup jalankan:

```bash
rdp upgrade
```
*(Catatan: Perintah ini akan menarik executable terbaru langsung dari GitHub rilis dan tidak akan mengubah file proyek lokal yang sedang Anda kerjakan).*

## Persyaratan Sistem
- Pastikan CLI `rdp` telah terpasang di sistem (dianjurkan diinstal secara global via `uv tool install rdp-cli`).
- Saat bekerja di dalam proyek, selalu pastikan *Virtual Environment* Python telah aktif (contoh: `source .venv/bin/activate` atau menggunakan perintah `uv run`).
