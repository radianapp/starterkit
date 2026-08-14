# Modul Single Sign-On (SSO)

Dokumen ini menjelaskan tentang implementasi Single Sign-On (SSO) pada RDP Starter Kit, beserta pengertian, manfaat, dan panduan lengkap cara mengonfigurasikannya.

## 1. Pengertian SSO
**Single Sign-On (SSO)** adalah metode autentikasi yang memungkinkan pengguna untuk masuk (login) ke berbagai aplikasi atau situs web menggunakan satu set kredensial (seperti akun Google, Microsoft, atau Apple). Dengan SSO, pengguna tidak perlu lagi menghafal banyak *username* dan *password* untuk setiap aplikasi yang berbeda.

Dalam konteks RDP Starter Kit, kita menggunakan akun **Google** sebagai penyedia layanan SSO utama.

## 2. Manfaat Menggunakan SSO
- **Keamanan Lebih Tinggi:** Karena autentikasi diserahkan kepada pihak ketiga (misal: Google), risiko pembobolan kata sandi akibat kelalaian aplikasi menjadi berkurang. Google telah menerapkan langkah-langkah keamanan canggih seperti MFA (Multi-Factor Authentication).
- **Pengalaman Pengguna (UX) Lebih Baik:** Pengguna dapat masuk ke sistem hanya dengan satu klik (One-Click Login) tanpa harus mengisi formulir pendaftaran yang panjang.
- **Efisiensi Manajemen Akun:** Pengguna tidak perlu mereset kata sandi jika lupa, karena akun dikelola oleh *provider* SSO. Jika akun Google perusahaan mereka dinonaktifkan, akses ke aplikasi Anda juga otomatis terputus.

## 3. Teknologi yang Digunakan
Starter Kit ini menggunakan **`django-allauth`**, pustaka standar emas (*gold standard*) di ekosistem Django untuk menangani autentikasi sosial dan registrasi.
- **Kenapa `django-allauth`?** Pustaka ini sangat matang, mendukung ratusan *provider* lain (Facebook, GitHub, Microsoft, dll), dan memiliki *adapter* yang fleksibel untuk kustomisasi bisnis logic (misalnya, menolak login selain dari email perusahaan tertentu).
- **Kenapa bukan Social Auth biasa?** Allauth menangani manajemen sesi, menghubungkan *Multiple Social Accounts* ke satu user Django, dan mengelola integrasi *signup* & *login* dengan sangat *seamless*.

## 4. Cara Mengonfigurasi & Contoh Penggunaan (Google Cloud)

Agar SSO Google dapat digunakan di aplikasi yang dihasilkan oleh StarterKit, Anda harus mendapatkan **Client ID** dan **Client Secret** dari Google Cloud Platform.

### A. Mendapatkan Kredensial dari Google Cloud Console
1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat Project baru atau gunakan *project* yang sudah ada.
3. Di bilah pencarian atas, cari **"APIs & Services"**, lalu masuk ke halaman tersebut.
4. Klik menu **OAuth consent screen** di bilah kiri.
   - Pilih *User Type*: **Internal** (jika hanya untuk organisasi Google Workspace Anda) atau **External** (jika untuk publik/siapa saja yang punya akun Google).
   - Isi informasi dasar aplikasi (Nama, Email *Support*).
   - Simpan dan Lanjutkan.
5. Pindah ke menu **Credentials** di bilah kiri.
6. Klik tombol **+ CREATE CREDENTIALS** di bagian atas, pilih **OAuth client ID**.
7. Pada menu *Application type*, pilih **Web application**.
8. Isi nama untuk *client* ini (misal: "App Production").
9. Di bagian **Authorized redirect URIs**, klik **+ ADD URI**. Tambahkan:
   - *Untuk Development/Lokal:* `http://127.0.0.1:8000/accounts/google/login/callback/`
   - *Untuk Production:* `https://[domain-aplikasi-anda.com]/accounts/google/login/callback/`
10. Klik **Create**.
11. Anda akan melihat sebuah _popup_ berisi **Client ID** dan **Client Secret**. Salin kedua nilai ini!

### 4. FAQ / Tanya Jawab Seputar SSO

### Apakah Project A dan Project B bisa "Nyambung"?
Secara default, **Ya untuk Identitasnya, tapi Tidak untuk Sesi (Session)-nya.**
- **Identitas Terpusat:** Pengguna hanya perlu satu akun Google perusahaan (`nama@perusahaan.com`) untuk masuk ke semua proyek yang menggunakan Starter Kit ini. Mereka tidak perlu mengingat password baru.
- **Sesi Terpisah:** Setiap proyek (misalnya Project A dan Project B) beroperasi secara independen dan memiliki _database_ masing-masing. Jika pengguna berhasil login di Project A, mereka tidak akan otomatis login di Project B. Mereka tetap harus mengklik tombol "Continue with Google" saat pertama kali membuka Project B agar akun pengguna baru dibuat di database Project B. 

### Bagaimana Jika Saya Tidak Ingin Menggunakan SSO di Proyek Tertentu?
Jika Anda membuat proyek baru (misalnya aplikasi untuk eksternal/publik) dan tidak ingin menyediakan opsi Google SSO, Anda cukup mematikannya di file `.env` tanpa harus menghapus atau memodifikasi satu baris kode pun!

Ubah nilai berikut di `.env`:
```env
ENABLE_GOOGLE_AUTH=False
```
**Efeknya:**
- Tombol **"Continue with Google"** akan otomatis disembunyikan dari antarmuka _Login_ dan _Register_.
- Pengguna hanya bisa mendaftar dan masuk secara konvensional (Email + Password).
- Anda tidak perlu menyiapkan _OAuth Client_ di Google Cloud Console untuk proyek tersebut.

### B. Cara Mengakali (Bypass) Kredensial untuk UI Development Lokal
Jika Anda sedang mendevelop tampilan UI dan belum sempat (atau tidak ingin) membuat *Client ID* di Google Cloud Console sungguhan, Anda bisa menggunakan kredensial palsu di `.env`:

```env
ENABLE_GOOGLE_AUTH=True
GOOGLE_CLIENT_ID="dummy-client-id-untuk-ui"
GOOGLE_CLIENT_SECRET="dummy-secret-untuk-ui"
```

> [!NOTE]
> **Penting**: Dengan kredensial palsu ini, tombol SSO akan muncul dengan normal di antarmuka `login` dan `register`. Anda bisa mendesain UI dengan bebas. Namun, jika tombol tersebut diklik, Anda akan mendapatkan halaman **Error 400 (invalid_request)** dari Google karena Client ID tersebut tidak dikenali. Ini wajar dan cukup untuk keperluan pengembangan tampilan saja.

### C. Menerapkan di Environment Aplikasi (`.env`)
Buka file `.env` di direktori *root* aplikasi (salin dari `.env.example` jika belum ada), dan ubah baris berikut jika sudah memiliki kredensial asli:

```env
ENABLE_USER_REGISTRATION=True
ENABLE_GOOGLE_AUTH=True
GOOGLE_CLIENT_ID="ISI_DENGAN_CLIENT_ID_DARI_GOOGLE"
GOOGLE_CLIENT_SECRET="ISI_DENGAN_CLIENT_SECRET_DARI_GOOGLE"
```

Ubah `ENABLE_GOOGLE_AUTH=True` agar tombol Google muncul di antarmuka *Login* dan *Register*.

### C. (Opsional) Membatasi Pendaftaran Hanya untuk Domain Tertentu
Sebagai *security guard*, Anda mungkin hanya ingin karyawan perusahaan Anda (misal `@radian.co.id`) yang bisa masuk.
Atur variabel ini di `.env`:

```env
ALLOWED_EMAIL_DOMAINS=radian.co.id
```

Jika ini diisi, meskipun seseorang berhasil *login* menggunakan akun Google pribadinya (misal `@gmail.com`), sistem RDP akan menggunakan `DomainRestrictAdapter` untuk menolak sesi tersebut karena domainnya tidak diizinkan.

## 5. Ringkasan Fitur SSO RDP
- **Auto-Registration:** Pendaftar pertama kali yang masuk via Google akan otomatis dibuatkan akun di sistem (`User` model) tanpa perlu konfirmasi manual lagi.
- **Fallback Login:** Jika pengguna sudah pernah mendaftar secara manual (dengan email dan password yang sama), `allauth` tetap mampu mencocokkan *Social Account* ke akun yang sudah ada (jika telah dikonfigurasi demikian, atau pengguna login manual dan melakukan *connect*).
- **Toggleable:** Hanya dengan mengubah `ENABLE_GOOGLE_AUTH=False` di `.env`, Anda dapat mematikan seluruh UI SSO tanpa perlu membongkar *source code* HTML.
