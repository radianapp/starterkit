# Code Map & Docs: User Registration (Pembuatan Akun)

**App Domain**: `accounts`  
**Event Category**: `Onboarding`  
**User Story Ref**: `US-004` (Register akun baru)

---

## 1. Developer View (Code Map & Tracing)

Pemetaan alur eksekusi dari HTTP Request hingga ke Database & Email Service.

### Entrypoint & Handlers
* **URL**: `/accounts/register/`
* **HTTP Method**: `GET` (Form Rendering), `POST` (Submit HTMX)
* **View Class**: `RegisterView` (`apps.accounts.views.auth.RegisterView`)
* **HTMX Target**: `#register-card-container`

### Execution Path (Function & Service Call Stack)
```text
[POST /accounts/register/]
 └── RegisterView.post(request)
      └── UserService.register_user(data=form.cleaned_data)
           ├── UserService._validate_registration_rules(data)
           ├── User.objects.create_user(username, email, password)
           ├── UserProfile.objects.create(user=user, avatar=...)
           └── EmailService.send_verification_email(user)
                └── django.core.mail.send_mail(...)
```

### Data Models & DB Queries
| Model | Operation | Description |
|---|---|---|
| `accounts.User` | `INSERT` | Membuat instance user baru |
| `accounts.UserProfile` | `INSERT` | Membuat profil bawaan |
| `accounts.EmailVerificationToken` | `INSERT` | Menyimpan token verifikasi (72 jam) |

### Telemetry & Resource Consumption Metrics
* **Expected Execution Time**: `80ms - 150ms`
* **Expected DB Queries**: `4 queries`
* **Service Units Consumed**: `0.0 units` (Free System Event)
* **External Calls**: `1 Email Gateway call`

---

## 2. User Guide (Panduan Pengguna)

### Cara Mendaftar Akun Baru
1. Buka halaman utama aplikasi dan klik tombol **"Daftar"** di sudut kanan atas navbar.
2. Isi form registrasi dengan data berikut:
   * **Email**: Email valid organisasi/pribadi.
   * **Password**: Minimal 8 karakter (kombinasi huruf & angka).
   * **Konfirmasi Password**: Harus cocok dengan password di atas.
3. Klik tombol **"Buat Akun Baru"**.
4. Sistem akan menampilkan notifikasi **"Registrasi Berhasil"** dan mengirimkan email verifikasi.
5. Cek kotak masuk (inbox/spam) email Anda dan klik tautan verifikasi untuk mengaktifkan akun.

---

## 3. FAQ (Pertanyaan Umum)

**Q: Mengapa saya tidak menerima email verifikasi?**  
*A: Pastikan email yang dimasukkan benar. Cek folder Spam/Junk. Jika tetap tidak ada, klik "Kirim Ulang Verification Email" di halaman login.*

**Q: Apakah saya bisa mendaftar dengan email publik (Gmail/Yahoo)?**  
*A: Tergantung konfigurasi `.env` domain restriction (`ALLOWED_EMAIL_DOMAINS`). Jika dibatasi, hanya email domain perusahaan yang diizinkan.*

---

## 4. Help & Troubleshooting (Pesan Error & Solusi)

| Error Code | HTTP Status | Pesan Error UI | Penyebab & Solusi |
|---|---|---|---|
| `EMAIL_ALREADY_EXISTS` | 422 | "Email ini sudah terdaftar." | Email sudah digunakan user lain. Gunakan menu Lupa Password jika lupa akun. |
| `WEAK_PASSWORD` | 422 | "Password terlalu mudah ditebak." | Password kurang dari 8 karakter atau terlalu sederhana. Gunakan kombinasi lebih kuat. |
| `EMAIL_SEND_FAILED` | 500 | "Gagal mengirim email verifikasi." | Layanan SMTP sedang gangguan. Hubungi administrator sistem. |
