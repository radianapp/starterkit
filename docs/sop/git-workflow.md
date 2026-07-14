# SOP Alur Kerja Git & Siklus Rilis (Git Workflow & Release)

Dokumen ini mendefinisikan standar manajemen branch dan konvensi git dalam proyek RDP Starter Kit.

## 1. Cabang (Branches)
- **`main`**: Berisi kode stabil yang siap dideploy ke produksi. Branch ini dilindungi (*protected*).
- **`develop`**: Branch integrasi utama untuk fitur-fitur baru.
- **`feature/US-XXX-deskripsi`**: Branch sementara untuk mengembangkan fitur spesifik berdasarkan User Story (US).
  - Contoh: `feature/US-040-git-workflow`

---

## 2. Konvensi Commit Message
Setiap commit **wajib** menyertakan nomor User Story (US) yang dikerjakan pada body commit, dan mengikuti spesifikasi Conventional Commits pada subject line.

### Format Commit:
```text
<type>(US-<nomor>): <deskripsi singkat di subject>

- <detail perubahan detail 1>
- <detail perubahan detail 2>
US: US-<nomor> — <judul story>
```

### Jenis Tipe (`<type>`):
- `feat`: Fitur baru.
- `fix`: Perbaikan bug.
- `docs`: Perubahan dokumentasi saja.
- `style`: Perubahan format kode, CSS, tanpa mengubah logika bisnis.
- `refactor`: Restrukturisasi kode tanpa mengubah fungsionalitas.
- `test`: Menambah atau memperbaiki unit test.

---

## 3. Pull Request & Integrasi
1. Developer membuat branch `feature/US-XXX`.
2. Developer melakukan commit perubahan dengan konvensi di atas.
3. Setelah unit test lokal berhasil dijalankan (`uv run pytest`), buat Pull Request (PR) ke branch `develop`.
4. GitHub Actions CI akan memverifikasi PR tersebut (linting, pytest, migration check).
5. Setelah disetujui, PR di-merge menggunakan metode **Squash and Merge** untuk menjaga riwayat git tetap bersih.
