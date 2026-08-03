# Mengelola Data Ekstra Secara Dinamis Menggunakan JSONField

RDP Starter Kit menggunakan `JSONField` pada profil pengguna (`UserProfile.extra_data`) untuk memfasilitasi penambahan kolom secara dinamis (seperti divisi, jabatan, nomor ekstensi, dsb.) terutama dari proses *Bulk Upload CSV*. 

Dengan fitur JSONB bawaan dari PostgreSQL (atau JSON1 di SQLite), Anda **TIDAK PERLU** membuat field manual atau melakukan `makemigrations/migrate` untuk sekadar membaca, memfilter, atau mensortir data-data ini.

Berikut adalah berbagai pola cara menanganinya:

## 1. Mengambil Data (Contoh: Menampilkan Divisi User)

**Di Level Python (Instance)**
Jika Anda sudah memiliki objek `user` (misalnya di *template* HTML atau view), perlakukan JSON field ini layaknya *dictionary* Python biasa:
```python
# Di View/Service Python
divisi = user.profile.extra_data.get('divisi', 'Tidak Ada Divisi')
```

**Di Template Django/Cotton**
Anda bisa mengakses properti JSON tersebut menggunakan dot notation khas Django template:
```html
{{ user.profile.extra_data.divisi|default:"Tidak Ada Divisi" }}
```

## 2. Mencari / Memfilter Data (Contoh: User di Divisi IT)

Gunakan *lookup* sintaks panah ganda (`__`) dari Django ORM. Django akan menerjemahkannya ke operator pencarian JSON database secara otomatis.

```python
# Mencari semua user yang divisinya adalah 'IT'
users_it = User.objects.filter(profile__extra_data__divisi='IT')

# Mencari user yang divisinya mengandung kata 'Data'
users_data = User.objects.filter(profile__extra_data__divisi__icontains='Data')
```

## 3. Mensortir Berdasarkan Field JSON

Anda bisa langsung melakukan pengurutan (*sorting*) berdasarkan *key* di dalam JSON.

### Cara Cepat (Mengurutkan Langsung)
```python
# Mengurutkan dari divisi A-Z, kemudian diurutkan lagi dari email A-Z
users = User.objects.all().order_by(
    'profile__extra_data__divisi', 
    'email' 
)
```

### Cara Advance (Menggunakan Annotate untuk DataTables/UI)
Gunakan `annotate` jika Anda ingin mengekstrak data dari dalam JSON menjadi seolah-olah "kolom nyata" untuk memudahkan pencarian lanjutan atau melemparnya ke UI.
```python
from django.db.models import F

users = User.objects.annotate(
    # Kita "ekstrak" key JSON menjadi kolom virtual bernama 'divisi'
    divisi=F('profile__extra_data__divisi')
).order_by('divisi', 'email')

# Sekarang Anda bisa memanggilnya langsung
# print(users[0].divisi)
```

---

## Kapan Anda Sebaiknya Membuat Field Manual?

Gunakan `extra_data` (JSONField) untuk kebutuhan pelengkap dan kolom yang sering berubah dinamis, namun sebaiknya Anda **membuat field konvensional di Models dan melakukan Migrate** HANYA JIKA:

1. **Relasi Data (Foreign Key):** Jika kolom divisi merujuk pada entri di tabel `Department` yang lain. JSON tidak mendukung integritas *Foreign Key* atau perilaku *Cascade Delete*.
2. **Kebutuhan Indexing Masif:** Anda memiliki data jutaan baris dan pencarian/pengurutan hampir selalu dilakukan *hanya* pada field ini saja. Meskipun PostgreSQL JSONB bisa menggunakan index GIN, field kolom nyata (*scalar type*) tetap lebih efisien dalam penggunaan *B-Tree index*.
3. **Validasi Tipe Data Ketat:** Atribut tersebut hanya boleh diisi dari daftar pilihan terbatas (membutuhkan `choices`), seperti `"IT"`, `"HR"`, atau `"FINANCE"`.
