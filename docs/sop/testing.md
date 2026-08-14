# SOP Pengujian Unit & Integrasi (Testing SOP)

Dokumen ini menjelaskan prosedur pengujian untuk memastikan setiap fitur baru memiliki coverage yang memadai sebelum digabungkan ke cabang utama.

## 1. Alat Pengujian
- **Pytest**: Runner utama pengujian (`uv run pytest`).
- **Pytest-Cov**: Menghitung cakupan kode (coverage).

---

## 2. Struktur Pengujian
- Letakkan seluruh file test di bawah direktori `tests/` dengan struktur subfolder yang meniru struktur aplikasi di bawah `apps/`.
  - Contoh: Pengujian view profil di `apps/accounts/views/profile.py` diletakkan di `tests/accounts/views/test_profile.py`.

---

## 3. Ketentuan Pengujian Wajib
- **TIDAK ADA** kode fitur baru yang digabungkan tanpa unit test.
- Target coverage minimum untuk kode di dalam folder `apps/` adalah **80%**.
- Setiap file test harus mengimpor konfigurasi dasar atau fixture dari `tests/conftest.py` jika memerlukan database atau user tiruan.

---

## 4. Cara Menjalankan Tes
Gunakan perintah berikut di terminal local:
```bash
# Menjalankan seluruh test suite
uv run pytest

# Menjalankan test dengan report coverage
uv run pytest --cov=apps -v
```
Jika ada tes yang gagal, perbaiki masalah tersebut terlebih dahulu sebelum melanjutkan proses development atau pembuatan Pull Request.

---

## 5. Referensi Tambahan
- Untuk panduan lengkap audit bug, false-positive detection, dan protokol diagnosa multi-lapis, lihat [Bug Audit & Quality Assurance](file:///docs/testing/bug-audit-and-quality-assurance.md).

