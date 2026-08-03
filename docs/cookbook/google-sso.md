# Implementasi Google SSO di RDP Starter Kit

Secara bawaan, RDP Starter Kit sudah menyiapkan tombol antarmuka (UI) untuk **"Continue with Google"** di halaman Login dan Register. Tombol ini dapat diaktifkan dengan mengubah `ENABLE_GOOGLE_AUTH=True` di file `.env`.

Namun, **logika autentikasinya (backend)** belum diimplementasikan karena tiap proyek membutuhkan kredensial Google Cloud (Client ID & Secret) yang berbeda-beda.

Dokumen ini akan memandu Anda mengimplementasikan Google SSO yang sesungguhnya menggunakan pustaka standar Django yaitu **`django-allauth`**.

---

## 1. Instalasi Pustaka

Gunakan `uv` untuk menambahkan `django-allauth`:

```bash
uv add django-allauth
```

## 2. Konfigurasi `config/settings/base.py`

Tambahkan pengaturan berikut di dalam `base.py`:

```python
# 1. Tambahkan ke INSTALLED_APPS
THIRD_PARTY_APPS = [
    # ... apps lainnya
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

# 2. Tambahkan Middleware
MIDDLEWARE = [
    # ... middleware lainnya
    "allauth.account.middleware.AccountMiddleware",
]

# 3. Konfigurasi Backend Autentikasi
AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend", # <--- Tambahkan ini
]

# 4. Konfigurasi Allauth & Kredensial Provider
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none" # Karena RDP sudah punya logic verifikasi sendiri
LOGIN_REDIRECT_URL = "/"

# Ambil kredensial dari .env
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env_var("GOOGLE_CLIENT_ID", ""),
            "secret": env_var("GOOGLE_CLIENT_SECRET", ""),
            "key": ""
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}
```

## 3. Tambahkan Kredensial di `.env`

Tambahkan baris berikut di file `.env` Anda:

```env
ENABLE_GOOGLE_AUTH=True
GOOGLE_CLIENT_ID="ISI_CLIENT_ID_DARI_GCP"
GOOGLE_CLIENT_SECRET="ISI_CLIENT_SECRET_DARI_GCP"
```

## 4. Konfigurasi Routing `config/urls.py`

Daftarkan *routing* milik `allauth` ke dalam URL utama:

```python
urlpatterns += [
    # ...
    path("accounts/", include("allauth.urls")),
]
```

## 5. Hubungkan Tombol UI ke Endpoint SSO

Buka kembali *template* Anda tempat tombol Google SSO berada:
1. `templates/accounts/login.html`
2. `templates/accounts/register.html`

Ubah tag `<button>` pada SSO menjadi tag `<a>` atau tambahkan *form method* yang mengarah ke URL `allauth`.

**Contoh untuk `login.html` & `register.html`:**

```html
{% load socialaccount %}

<a href="{% provider_login_url 'google' %}" class="auth-sso-btn" style="text-decoration:none;">
    <!-- SVG Icon Google -->
    Continue with Google
</a>
```

*(Catatan: Tombol secara visual sudah di-styling oleh RDP CSS agar tampak seperti tombol meskipun ia menggunakan tag `<a>`).*

## 6. Setup di Google Cloud Console

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat Project baru atau gunakan yang sudah ada.
3. Masuk ke menu **APIs & Services > Credentials**.
4. Klik **Create Credentials > OAuth client ID**.
5. Pilih **Web application**.
6. Tambahkan **Authorized redirect URIs**:
   - Untuk Development: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - Untuk Production: `https://[domain-anda.com]/accounts/google/login/callback/`
7. Salin **Client ID** dan **Client Secret** yang dihasilkan, lalu masukkan ke file `.env` Anda.

## 7. Migrasi Database

Terakhir, jalankan migrasi agar `django-allauth` membuat tabel-tabel pendukung yang dibutuhkannya:

```bash
uv run python manage.py migrate
```

Selesai! Sekarang Anda sudah memiliki sistem Single Sign-On (SSO) Google bertaraf *Enterprise* yang siap digunakan oleh para pengguna aplikasi.
