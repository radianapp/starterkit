# ERD — RDP Starter Kit

> Wajib diupdate setiap kali file di `models/` berubah (tambah model, tambah field, ubah relasi).

## Diagram

```mermaid
erDiagram
    USER {
        bigint id PK
        string email UK
        string username
        string first_name
        string last_name
        bool is_active
        bool is_staff
        bool email_verified
        datetime email_verified_at
        datetime created_at
        datetime updated_at
    }

    USER_PROFILE {
        bigint id PK
        bigint user_id FK
        string avatar
        string bio
        datetime created_at
        datetime updated_at
    }

    ACTIVITY {
        bigint id PK
        bigint user_id FK
        string title
        string description
        string status
        decimal amount
        datetime created_at
    }

    USER ||--|| USER_PROFILE : "has one"
    USER ||--o{ ACTIVITY : "has many"
```

## Catatan

- `USER.email` digunakan sebagai `USERNAME_FIELD` (login dengan email)
- `USER_PROFILE` dibuat otomatis via signal saat `USER` baru dibuat
