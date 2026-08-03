# RDP UI Components Guide

RDP UI adalah sistem desain kustom yang dibangun di atas Django Cotton dan variabel CSS murni tanpa build step.

## Cara Menggunakan Komponen (Phase 4.1 & 4.2)

### 1. Primitives & Feedback
Gunakan komponen Cotton bawaan RDP UI untuk elemen primitif dan umpan balik:

- **Button**: `<c-rdp.button variant="primary" size="md">Simpan</c-rdp.button>`
  - *Tip: Tambahkan atribut `href` untuk merender button sebagai tautan (`<a>`):* `<c-rdp.button href="/dashboard/">Buka Dashboard</c-rdp.button>`
- **Badge**: `<c-rdp.badge variant="success" pill="True">Active</c-rdp.badge>`
- **Alert**: `<c-rdp.alert variant="warning" title="Perhatian">Sistem akan maintenance.</c-rdp.alert>`
- **Toast**: `<c-rdp.toast title="Sukses">Data berhasil disimpan.</c-rdp.toast>`
- **Progress**: `<c-rdp.progress value="45" />`
- **Spinner/Skeleton**: `<c-rdp.spinner size="sm" />` atau `<c-rdp.skeleton />`

### 2. Forms & Controls
Elemen form secara otomatis didukung oleh styling RDP UI dengan layout yang rapi:

- **Text Input**: `<c-rdp.form.input name="email" label="Email" help_text="Masukkan email kerja." />`
- **Textarea**: `<c-rdp.form.textarea name="notes" label="Catatan">Isi...</c-rdp.form.textarea>`
- **Select**: 
  ```html
  <c-rdp.form.select name="role" label="Role">
    <option value="1">Admin</option>
  </c-rdp.form.select>
  ```
- **File Upload**: `<c-rdp.form.file name="doc" label="Unggah Dokumen" />`
- **Selection**: 
  `<c-rdp.form.checkbox name="agree" label="Setuju" />`
  `<c-rdp.form.radio name="opsi" label="Opsi 1" />`
  `<c-rdp.form.switch name="toggle" label="Aktifkan" />`

Semua komponen form sudah siap digunakan bersama dengan integrasi error handling (HTMX 422) secara otomatis.

### 3. Overlays & Navigation (Phase 4.3)
Untuk navigasi yang kompleks dan overlay, RDP UI menggunakan Alpine.js untuk transisi dan manajemen status yang murni di sisi klien:

- **Modal**:
  ```html
  <c-rdp.modal title="Judul Modal" size="md">
    <c-slot name="trigger">
      <c-rdp.button>Buka Modal</c-rdp.button>
    </c-slot>
    Isi modal di sini.
  </c-rdp.modal>
  ```
- **Drawer**: Gunakan komponen `<c-rdp.drawer title="Menu" side="right">...</c-rdp.drawer>` untuk panel dari samping.
- **Dropdown**: Gunakan komponen `<c-rdp.dropdown align="left">...</c-rdp.dropdown>` untuk menu aksi.
- **Tabs**: 
  ```html
  <c-rdp.tabs>
    <c-slot name="tab_list">
      <button class="rdp-tabs__tab" @click="activeTab = 0">Tab 1</button>
      <button class="rdp-tabs__tab" @click="activeTab = 1">Tab 2</button>
    </c-slot>
    <div x-show="activeTab === 0">Konten Tab 1</div>
    <div x-show="activeTab === 1">Konten Tab 2</div>
  </c-rdp.tabs>
  ```

### 4. Data Display (Phase 4.4)
Untuk menyajikan data terstruktur:

- **Card**:
  ```html
  <c-rdp.card title="Pengaturan">
    <p>Deskripsi...</p>
    <c-slot name="footer">
      <c-rdp.button>Simpan</c-rdp.button>
    </c-slot>
  </c-rdp.card>
  ```
  - *Tip: Gunakan argumen `clickable="True"` beserta `href="URL"` untuk merender keseluruhan kartu sebagai tautan `<a>`.*
- **Stat Card**: `<c-rdp.stat_card label="Pendapatan" value="$1,200" trend="+5%" trend_up="True" />`
- **Accordion**: `<c-rdp.accordion title="Detail">Konten tersembunyi...</c-rdp.accordion>`
- **Timeline**:
  ```html
  <c-rdp.timeline>
    <c-rdp.timeline_item title="Laporan Baru" time="Baru saja" active="True">
      Laporan penjualan kuartal ini.
    </c-rdp.timeline_item>
  </c-rdp.timeline>
  ```
  ```
- **Empty State**: `<c-rdp.empty_state title="Belum ada data" description="Mulai dengan menambah data pertama Anda." />`

### 5. Layout & Responsive Behavior (Phase 4.5)
RDP UI menyediakan Holy Grail layout melalui `<c-layout.app>` yang otomatis beradaptasi dengan berbagai ukuran layar (Responsive Strategy):

- **Mobile (< 768px)**: 
  - Sidebar tersembunyi (Drawer) yang dapat dibuka via ikon Hamburger.
  - Search box otomatis pindah ke bagian atas di dalam Sidebar.
  - Saat Sidebar terbuka, akan ada lapisan gelap (scrim/overlay) transparan di belakangnya. Klik area gelap ini akan menutup sidebar secara otomatis.
- **Tablet (768px - 1023px)**: 
  - Sidebar tampil permanen dengan ukuran lebar standar `224px`.
  - Tombol Hamburger di-hide karena sidebar sudah terbuka.
  - Search box tampil di Topbar.
- **Desktop (≥ 1024px)**: 
  - Sidebar penuh dan fitur *Manual Collapse* (memperkecil Sidebar menjadi *Icon Rail* 64px) diaktifkan melalui tombol ⟨ Collapse di sudut bawah Sidebar.

### 6. Theme Switcher (Dark/Light Mode)
RDP UI didukung *CSS Variables/Color Tokens* canggih dengan sinkronisasi ke PicoCSS `data-theme`. Komponen `<button @click="toggleDarkMode()">` di Topbar (Navbar) sudah dikonfigurasi untuk secara otomatis merubah background (`light/dark`) sekaligus menukar *Color Tokens* agar teks dan elemen UI lain tidak hilang / tidak terbaca akibat pergantian warna dasar.

## Konsep Framework & Arsitektur

RDP Framework dirancang dengan filosofi **"Own Your Code"** yang dipadukan dengan **"Upgradeable Core"** (terinspirasi dari ekosistem modern).

1. **Komponen UI (Copy-Paste / Scaffolding)**: Komponen UI (seperti file-file di `templates/cotton/`) beserta template dasar disalin langsung ke dalam proyek pengguna. Pengguna memegang kendali penuh (bebas mengubah struktur, gaya CSS, atau logika komponen tersebut, misalnya merombak total tampilan halaman *Login*).
2. **Core Engine**: Fungsionalitas inti (seperti base models, integrasi HTMX bawaan) dan *tooling* (CLI `rdp`) dipisahkan sebagai ketergantungan (dependency) yang dapat diperbarui secara terpusat.
3. **Bagaimana jika pengguna mengubah kode template (misal login) dan ada *upgrade*?** 
   Karena file template dan komponen UI disalin secara fisik ke dalam kode aplikasi pengguna (`templates/`), perubahan pengguna **tidak akan tertimpa** secara paksa saat pengguna menaikkan versi framework. Jika tim RDP merilis pembaruan atau perbaikan keamanan pada komponen bawaan, pengguna dapat menggunakan CLI `rdp` untuk melihat perbedaan (*diff*) dan memilih untuk melakukan *merge* secara manual atau menolak pembaruan komponen tersebut.

## Alur Kerja (Workflow) & Panduan Penggunaan

### 1. Dari Sisi Pembuat Framework (Developer/Maintainer RDP)
Alur untuk merawat, memperbarui, dan mendistribusikan framework RDP ke publik/tim internal:

- **Menaikkan Versi (Versioning) & Rilis:**
  1. Lakukan perubahan pada kode *starterkit* atau *core*.
  2. Pastikan semua *Unit Test* berhasil berjalan: `uv run pytest`.
  3. Perbarui versi di dalam `pyproject.toml` (contoh: dari versi `0.1.0` ke `0.2.0`).
  4. Lakukan *commit* dengan pesan standar: `git commit -m "chore: bump version to 0.2.0"`.
  5. Buat penanda versi (*tag*): `git tag v0.2.0`.
- **Push ke GitHub & Distribusi:**
  1. Dorong perubahan kode utama: `git push origin main`.
  2. Dorong tag rilis ke GitHub: `git push origin v0.2.0`.
  3. (Opsional) Sistem CI/CD (seperti GitHub Actions) akan menangkap tag baru tersebut, mem-build paket (jika didistribusikan via PyPI), dan memperbarui *template repository*.

### 2. Dari Sisi Pengguna (Pengembang Aplikasi)
Alur untuk programmer atau pengguna yang ingin menggunakan RDP Framework untuk membangun aplikasi baru:

- **Instalasi Framework RDP Baru:**
  Pendekatan yang disarankan adalah menggunakan alat baris perintah (CLI) bawaan yaitu `rdp`.
  1. Pastikan **Python** dan **`uv`** sudah terinstal.
  2. Pasang CLI RDP di sistem lokal secara global (asumsi paket bernama `rdp-cli`):
     ```bash
     uv tool install rdp-cli
     ```
  3. Buat proyek baru berdasarkan versi RDP terbaru:
     ```bash
     rdp init nama_proyek_anda
     ```
     *Proses ini akan mengkloning struktur "starterkit" secara otomatis, menghapus riwayat `.git` asal, dan mengatur ulang nama proyek.*
  4. Masuk ke proyek dan aktifkan environment `uv`:
     ```bash
     cd nama_proyek_anda
     uv sync
     source .venv/bin/activate  # (atau .venv\Scripts\activate di Windows)
     ```

- **Menggunakan CLI `rdp` dalam Pengembangan:**
  CLI `rdp` didesain untuk menyederhanakan tugas-tugas berulang:
  - `rdp add <komponen>`: Mengambil spesifik UI komponen ke dalam folder lokal proyek (contoh: `rdp add modal`, `rdp add datatable`). Karena disalin ke ruang proyek (konsep "Own Your Code"), komponen ini bebas dioprek tanpa takut rusak saat update.
  - `rdp update`: Memeriksa pembaruan versi *core* atau komponen. Jika ada komponen UI lokal yang sudah diubah secara signifikan oleh pengguna, CLI akan memberi tahu dan memberikan opsi untuk menimpa, mengabaikan, atau menampilkan file perbedaan (*diff*).
  - `rdp serve`: Pintasan untuk menjalankan server pengembangan sekaligus melakukan hot-reload (mirip `python manage.py runserver`).
  - `rdp make-component <nama>`: Membuat struktur dasar (skeleton) komponen Cotton baru secara instan di dalam `templates/cotton/`.

---

## Sistem Versi & Changelog

### Memahami Versi Framework vs Versi Lokal

RDP Starter Kit memiliki dua variabel versi yang berbeda:

| Variabel | Deskripsi | Di mana diset |
|---|---|---|
| `FRAMEWORK_VERSION` | Versi dari *template sumber* di GitHub | `.env` (diisi developer saat clone) |
| `LOCAL_APP_VERSION` | Versi *aplikasi Anda* sendiri | `.env` (diupdate setiap deploy baru) |

Contoh isi `.env`:
```ini
# Versi framework yang Anda pakai dari GitHub
FRAMEWORK_VERSION=0.3.0

# Versi aplikasi lokal Anda (update setiap rilis baru)
LOCAL_APP_VERSION=1.2.0
```

### Melihat Changelog

1. Login ke aplikasi.
2. Buka sidebar → klik **Changelog**.
3. Atau akses langsung: `/changelog/`

Di halaman ini, Anda akan melihat:
- **Version Info Bar** — menampilkan versi framework dan versi lokal secara berdampingan.
- **Daftar log pembaruan** — setiap entri memuat versi, judul, tipe update, dan deskripsi.

### Menambah Log Pembaruan (Admin)

1. Masuk ke Admin Panel (`/admin/`).
2. Pilih **Dashboard → System Updates → + Add**.
3. Isi:
   - **Version**: versi rilis (contoh: `v1.2.0`).
   - **Title**: judul singkat pembaruan.
   - **Description**: penjelasan apa yang berubah.
   - **Update Type**: pilih antara `Core Update`, `Page Update`, `Bugfix`, atau `New Feature`.
4. Simpan → entri langsung muncul di halaman Changelog.

### Konvensi Versi

Gunakan format **Semantic Versioning** (`MAJOR.MINOR.PATCH`):
- `MAJOR` — perubahan besar yang memutus kompatibilitas.
- `MINOR` — fitur baru yang backward-compatible.
- `PATCH` — perbaikan bug kecil.

## Fitur Manajemen Pengguna

### 1. Bulk Upload via CSV (Hanya Superadmin)
Fitur Bulk Upload memungkinkan Superadmin untuk menambahkan banyak pengguna sekaligus melalui file CSV.
- **Langkah-langkah**:
  1. Buka halaman **Manajemen User** di interface dashboard.
  2. Klik tombol **Upload CSV**.
  3. Pilih file CSV (wajib memiliki kolom `email`, opsional `password`, `first_name`, `last_name`, serta kolom tambahan lain yang akan disimpan sebagai *custom fields* di `extra_data`).
- **Pemrosesan Skala Besar**: Jika jumlah baris lebih dari 1000, proses akan otomatis dialihkan ke *background task* (Celery) agar sistem tidak terblokir.
- **Notifikasi Email**: Pengguna akan mendapatkan email invitasi berisi tautan untuk mengaktifkan akun mereka (tautan valid selama 24 jam).
- **Keamanan Akun**: Pengguna hasil Bulk Upload akan dipaksa (*forced*) mengganti password default atau password acak mereka pada saat pertama kali berhasil login.

### 2. Mengirim Ulang Email Undangan (Resend Invite)
Jika pengguna belum login atau mengaktifkan akunnya dari email invitasi, admin dapat mengirim ulang email tersebut:
- Di tabel Manajemen User, klik tombol **Resend Invite** pada baris pengguna yang statusnya *Pending* atau belum login sama sekali.
