# Panduan Implementasi Centralized Identity (OIDC)

Dokumen ini berisi prosedur *step-by-step* untuk menghubungkan **RDP Starter Kit** ke **Centralized Identity Server** (seperti **Keycloak**, **Authelia**, atau **Authentik**). Ini ditujukan sebagai *knowledge base* jika di masa depan Anda memutuskan untuk mengubah arsitektur aplikasi menjadi *Single Session*.

Pendekatan termudah dan paling berstandar industri adalah menggunakan protokol **OpenID Connect (OIDC)**, yang didukung secara *native* oleh pustaka `django-allauth` yang sudah terpasang di *Starter Kit*.

---

## Prasyarat
1. Anda sudah mendeploy peladen Identity Server terpusat (contoh: Keycloak) di URL tertentu, misal: `https://auth.rdp.co.id`.
2. Proyek *Starter Kit* Anda beroperasi, misal di `https://admin.rdp.co.id`.

---

## Langkah 1: Setup di Sisi Identity Server (Keycloak)
Sebelum menyentuh kode *Starter Kit*, Anda perlu mendaftarkan aplikasi Anda di *Identity Server*.

1. Masuk ke dasbor Admin Keycloak.
2. Buat **Client** baru (misal: `rdp-admin-app`).
3. Set protokol menjadi **openid-connect**.
4. Set *Access Type* menjadi **confidential**.
5. Konfigurasikan **Valid Redirect URIs** untuk menunjuk ke aplikasi Anda:
   - `https://admin.rdp.co.id/accounts/oidc/keycloak/login/callback/`
6. Simpan, lalu buka tab **Credentials** untuk menyalin **Client ID** dan **Client Secret**.
7. Catat URL penemuan OIDC Anda (biasanya `https://auth.rdp.co.id/realms/[nama-realm]/.well-known/openid-configuration`).

---

## Langkah 2: Konfigurasi di Sisi Starter Kit (`settings.py`)
Sekarang, kita mengonfigurasi Django agar membaca *server* tersentral tersebut.

Buka `config/settings/base.py` dan perbarui pengaturan `SOCIALACCOUNT_PROVIDERS`:

```python
# Tambahkan konfigurasi OpenID Connect di dalam dictionary providers
SOCIALACCOUNT_PROVIDERS = {
    # ... (opsional) konfigurasi google yang sudah ada
    
    # Tambahkan block ini:
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "keycloak",
                "name": "Keycloak SSO",
                "client_id": env_var("OIDC_CLIENT_ID", ""),
                "secret": env_var("OIDC_CLIENT_SECRET", ""),
                "settings": {
                    "server_url": env_var("OIDC_SERVER_URL", "https://auth.rdp.co.id/realms/rdp"),
                },
            }
        ]
    }
}
```

Kemudian, tambahkan variabel lingkungan di `.env` aplikasi Anda:
```env
OIDC_CLIENT_ID="rdp-admin-app"
OIDC_CLIENT_SECRET="secret-dari-keycloak"
OIDC_SERVER_URL="https://auth.rdp.co.id/realms/rdp"
```

---

## Langkah 3: Mengarahkan (Redirect) Login Bawaan ke Server Sentral
Karena ini adalah *Centralized Identity*, pengguna tidak boleh melihat formulir pendaftaran atau login bawaan *Starter Kit*. Mereka harus langsung dilempar ke *Server Sentral*.

Kita harus mengubah alur `user_login` di `apps/accounts/views/login.py`:

```python
from django.shortcuts import redirect
from allauth.socialaccount.providers.openid_connect.provider import OpenIDConnectProvider

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    
    # Alihkan SEMUA percobaan login ke Keycloak secara otomatis
    # 'keycloak' adalah provider_id yang kita atur di pengaturan sebelumnya
    from allauth.socialaccount.templatetags.socialaccount import provider_login_url
    
    # Redirect pengguna ke URL autentikasi OIDC
    return redirect("socialaccount_login", provider_id="keycloak")
```
Lakukan hal yang sama pada fungsi pendaftaran (`user_register` atau `register_wizard`) agar aplikasi lokal menolak pendaftaran akun secara langsung.

---

## Langkah 4: Sinkronisasi Profil (Opsional)
Ketika *user* kembali dari Keycloak ke *Starter Kit* membawa token JWT, *Starter Kit* akan otomatis membuatkan *user* di basis data lokal jika belum ada. 

Jika Anda ingin menarik _role_, departemen, atau data lain dari Keycloak ke _Starter Kit_, Anda dapat menggunakan _Signal_ bawaan dari `allauth`. Tambahkan kode ini di `apps/accounts/signals.py`:

```python
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

@receiver(pre_social_login)
def populate_user_from_oidc(sender, request, sociallogin, **kwargs):
    # Mengambil data payload dari token Keycloak
    user_data = sociallogin.account.extra_data
    
    # Isi properti profil lokal dengan data dari pusat
    user = sociallogin.user
    if not user.id:  # Jika ini pengguna baru
        user.first_name = user_data.get("given_name", "")
        user.last_name = user_data.get("family_name", "")
        # Misal Keycloak mengirim klaim custom 'department'
        # Anda bisa menyimpannya ke user.profile
```

---

## Langkah 5: Logout Terpusat (Single Logout)
Tantangan terbesar sistem sentral adalah ketika pengguna _logout_. Jika *user* menekan tombol *logout* di Project A, sesi mereka di Project A akan mati, tetapi **sesi di Server Sentral (Keycloak) masih hidup**. Akibatnya, jika mereka kembali ke halaman _login_, mereka akan dipaksa masuk kembali secara otomatis.

Untuk mencegahnya, Anda harus memodifikasi fungsi _logout_ di `apps/accounts/views/login.py`:

```python
from django.contrib.auth import logout
import urllib.parse

def user_logout(request):
    # 1. Matikan sesi lokal
    logout(request)
    
    # 2. Redirect ke Server Sentral untuk mematikan sesi global
    # Format URL tergantung OIDC Provider, contoh untuk Keycloak:
    oidc_logout_url = "https://auth.rdp.co.id/realms/rdp/protocol/openid-connect/logout"
    redirect_uri = request.build_absolute_uri('/') # Setelah logout kembali ke Home
    
    url = f"{oidc_logout_url}?post_logout_redirect_uri={urllib.parse.quote(redirect_uri)}"
    
    return redirect(url)
```

Dengan langkah-langkah di atas, aplikasi *Starter Kit* Anda akan berubah dari identitas otonom menjadi identitas tersentralisasi (SSO penuh) menggunakan OpenID Connect!
