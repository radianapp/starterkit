# SOP Pendokumentasian Modul (Module Documentation SOP)

Dokumen ini menjelaskan standar dalam mendokumentasikan modul-modul aplikasi baru di dalam direktori `docs/modules/`.

## 1. Lokasi Dokumentasi Modul
- Setiap modul utama (misalnya modul `billing`, `notifications`, `analytics`) wajib memiliki satu file panduan di bawah `docs/modules/{nama-modul}.md`.

---

## 2. Struktur Konten Panduan Modul
Setiap panduan modul harus memiliki struktur berikut:

1. **Deskripsi Ringkas**: Penjelasan apa fungsi dari modul tersebut.
2. **Arsitektur & Model**: Daftar model yang terpengaruh beserta relasinya (bisa berupa teks atau Mermaid ERD).
3. **Bisnis Logic (Services)**: Penjelasan mengenai file `services/` di dalam modul dan fungsi-fungsi penting yang ada di dalamnya.
4. **Endpoint API / Views**: Menjelaskan URL yang terekspos serta kegunaannya.
5. **Konvensi Khusus**: Aturan khusus yang hanya berlaku untuk modul ini (misal: format payload eksternal untuk API payment gateway).

---

## 3. Tanggung Jawab Pembaruan
- Developer yang menambahkan atau merombak fungsionalitas di dalam modul **wajib** memperbarui file dokumentasi terkait sebelum menyelesaikan tugasnya.
