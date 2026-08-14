# Code Map & Tracing Matrix: Otentikasi & Manajemen Akun

Dokumen ini mendokumentasikan pemetaan kode lengkap (*Code Map*) untuk alur **Otentikasi & Manajemen Akun** pada RDP StarterKit.

---

## 1. Tracing Matrix: User Journey & System Lifecycle

### A. Registrasi Akun Baru (`US-004`, `US-008`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Akses Form Register | `/account/register/` (`accounts:register`) | [RegisterView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/register.py#L40) | - | - | HTTP 200 GET | `[x]` |
| 2 | Submit Email (Step 1) | `hx-post="/account/register/"` | [RegisterView.post](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/register.py#L65) | [user_service.py](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/user_service.py) | `User` | `HX-Trigger: step2` | `[x]` |
| 3 | Submit Password (Step 2) | `hx-post="/account/register/"` | [RegisterView.post](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/register.py#L85) | [create_user_service](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/user_service.py) | `User`, `UserProfile` | `ExecutionTraceLog` | `[x]` |
| 4 | Kirim Email Verifikasi | Triggered on user save | - | [send_verification_email](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/email_service.py) | `User` (email_verified=False) | Console / SMTP Log | `[x]` |
| 5 | Klik Link Email Verifikasi | `/account/verify/<token>/` | [VerifyEmailView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/verify_email.py) | [verify_user_email](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/email_service.py) | `User.email_verified=True` | `UserActivityLog` | `[x]` |

---

### B. Otentikasi Login, Passkeys, & Session (`US-005`, `US-006`, `US-018`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Form Login Kredensial | `/account/login/` (`accounts:login`) | [LoginView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/login.py) | `auth_service.py` | `User` | HTTP 200 / 422 | `[x]` |
| 2 | Login dengan Passkey | `hx-post="/account/webauthn/login/verify/"` | [login_verify](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/webauthn.py) | [webauthn_service.py](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/webauthn_service.py) | `PasskeyCredential` | `UserActivityLog` | `[x]` |
| 3 | Mendaftarkan Passkey Baru | `hx-post="/account/webauthn/register/verify/"` | [register_verify](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/webauthn.py#L33) | [verify_and_save_registration](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/webauthn_service.py) | `PasskeyCredential` | `HX-Trigger: passkeyRegistered` | `[x]` |
| 4 | Logout Session | `/account/logout/` (`accounts:logout`) | `LogoutView` | Django Auth Logout | Session Flush | `UserActivityLog` | `[x]` |

---

### C. Reset Password & Password Harus Ganti (`US-007`, `US-025`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Request Reset Password | `/account/password/reset/` | `PasswordResetView` | [send_password_reset_email](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/email_service.py) | Token TokenGenerator | Mailer Log | `[x]` |
| 2 | Paksa Ganti Password (Force Reset) | `/account/password/force-change/` | `ForcePasswordChangeView` | `user_service.py` | `UserProfile.extra_data` | `ForceChangePasswordMiddleware` | `[x]` |

---

### D. Bulk Upload Users (`US-025`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Upload CSV User oleh Admin | `/dashboard/users/bulk-upload/` | [UserBulkUploadView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/users.py) | [process_bulk_users](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/user_service.py#L58) | `User`, `UserProfile` | `process_bulk_users_task` (Celery) | `[x]` |

---

## 2. Struktur Komponen Codebase Accounts

```text
apps/accounts/
├── admin/                     ← Django Admin Customs (UserAdmin, PasskeyAdmin)
├── forms/                     ← Form Validasi (Login, Register, Profile, BulkUpload)
├── middleware.py              ← ForceChangePasswordMiddleware
├── models/                    ← Database Entities:
│   ├── user.py                ← Custom User model (AbstractUser)
│   ├── profile.py             ← UserProfile (avatar, bio, extra_data JSON)
│   └── passkey.py             ← PasskeyCredential (WebAuthn credentials)
├── services/                  ← Business Logic Layer (Terisolasi dari View):
│   ├── email_service.py       ← SMTP Email Verification & Password Reset
│   ├── user_service.py        ← User Creation, Bulk Import, Force Reset
│   └── webauthn_service.py    ← FIDO2/WebAuthn Challenge & Signature Verification
└── views/                     ← Class-Based & Function-Based Views (HTMX Partial Supported)
```
