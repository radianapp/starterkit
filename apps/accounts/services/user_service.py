"""
Service layer untuk user management.
US: US-004 — Register akun baru
US: US-003 — Custom User model siap pakai

TUJUAN: Logic bisnis pembuatan user — dipisahkan dari view agar bisa dipanggil
dari view, Celery task, atau management command tanpa duplikasi.

ALUR:
  1. Terima data dari wizard (email, password, extra)
  2. Buat User via create_user()
  3. Update UserProfile.extra_data dengan jawaban wizard
  4. Return user yang sudah dibuat
"""

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_from_wizard(email: str, password: str, extra: dict) -> "User":
    """
    TUJUAN: Buat User + UserProfile dari data registration wizard.

    ALUR:
      1. create_user() → signal post_save → UserProfile auto-created
      2. Update profile.extra_data dengan jawaban custom steps
      3. Return user

    DIPANGGIL DARI: apps.accounts.views.register.register_wizard (step password)
    DEPENDENSI: apps.accounts.models.User, apps.accounts.signals (auto-create profile)

    # 🧪 TEST MANUAL: Cek di Django shell:
    #   from apps.accounts.services.user_service import create_user_from_wizard
    #   u = create_user_from_wizard("test@x.com", "pass1234", {"org": "RDP"})
    #   assert u.profile.extra_data == {"org": "RDP"}
    """
    # Import di dalam fungsi untuk hindari circular import pada test
    from apps.accounts.models import UserProfile

    # Gunakan email sebagai username — unique constraint di User.email sudah cukup
    user = User.objects.create_user(
        email=email,
        password=password,
        username=email,
    )

    if extra:
        # Signal sudah buat profile kosong — update extra_data saja
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.extra_data = extra
        profile.save(update_fields=["extra_data"])

    return user


def process_bulk_users(rows: list, request=None) -> dict:
    """
    TUJUAN: Proses list of dictionary (dari CSV) untuk bulk insert user.
    
    ALUR:
      1. Loop setiap baris.
      2. Ekstrak email, first_name, last_name, password.
      3. Kolom lainnya dimasukkan ke extra_data.
      4. Generate random password jika kosong.
      5. Set must_change_password=True di extra_data.
      6. Buat user (bulk atau satu per satu dengan atomic transaction).
      7. Kirim email verifikasi/invite.
    """
    from django.db import transaction
    from django.utils.crypto import get_random_string
    from apps.accounts.models import UserProfile
    from apps.accounts.services.email_service import send_verification_email
    
    results = {"success": 0, "failed": 0, "errors": []}
    
    for idx, row in enumerate(rows):
        email = row.get("email", "").strip()
        if not email:
            results["failed"] += 1
            results["errors"].append(f"Baris {idx+1}: Email kosong.")
            continue
            
        if User.objects.filter(email=email).exists():
            results["failed"] += 1
            results["errors"].append(f"Baris {idx+1}: Email {email} sudah terdaftar.")
            continue

        first_name = row.pop("first_name", "").strip()
        last_name = row.pop("last_name", "").strip()
        
        # Ambil password atau generate random
        password = row.pop("password", "").strip()
        if not password:
            password = get_random_string(length=12)

        # Sisanya adalah custom fields
        row.pop("email", None) # Hapus email dari sisa
        extra_data = row
        extra_data["must_change_password"] = True

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    username=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                
                profile, _ = UserProfile.objects.get_or_create(user=user)
                
                # Merge existing extra_data with new extra_data (in case signal created some)
                if isinstance(profile.extra_data, dict):
                    profile.extra_data.update(extra_data)
                else:
                    profile.extra_data = extra_data
                
                profile.save(update_fields=["extra_data"])
                
                # Send verification email
                if request:
                    send_verification_email(user, request)
                
                results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Baris {idx+1} ({email}): {str(e)}")

    return results
