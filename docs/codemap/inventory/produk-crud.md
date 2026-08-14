# Code Map & Docs: Produk CRUD Management

**App Domain**: `inventory`  
**Event Category**: `CRUD Management`  
**User Story Ref**: `US-CRUD-PRODUK`

---

## 1. Developer View (Code Map & Tracing)

Pemetaan alur eksekusi lengkap untuk operasi CRUD pada entity **Produk**.

### Model Attributes & Fields
* **Model Class**: `apps.inventory.models.Produk`
* **Table Name**: `inventory_produk`
* **Fields**: `id` (BigAutoField), `nama` (CharField), `sku` (CharField), `kategori` (ForeignKey), `harga` (DecimalField), `stok` (IntegerField), `pemasok` (ForeignKey), `deskripsi` (TextField), `status` (CharField), `created_at` (DateTimeField), `updated_at` (DateTimeField)

---

### Operations Breakdown

#### A. Read / List & Search (`GET /inventory/produks/`)
* **View Class**: `ProdukListView` (`apps.inventory.views.produk.ProdukListView`)
* **Execution Path**:
  ```text
  [GET /inventory/produks/]
   └── ProdukListView.get(request)
        └── ProdukService.get_paginated_list(search_query, filter_params)
             └── Produk.objects.filter(...).select_related(...)
  ```
* **Expected Metrics**: `execution_time: ~20ms`, `db_queries: 2`

#### B. Create / Add Entity (`POST /inventory/produks/create/`)
* **View Class**: `ProdukCreateView` (`apps.inventory.views.produk.ProdukCreateView`)
* **Execution Path**:
  ```text
  [POST /inventory/produks/create/]
   └── ProdukCreateView.post(request)
        └── ProdukService.create_produk(form_data)
             ├── ProdukForm.is_valid()
             └── Produk.objects.create(...)
  ```
* **Expected Metrics**: `execution_time: ~45ms`, `db_queries: 3`

#### C. Update / Edit Entity (`POST /inventory/produks/<id>/edit/`)
* **View Class**: `ProdukUpdateView` (`apps.inventory.views.produk.ProdukUpdateView`)
* **Execution Path**:
  ```text
  [POST /inventory/produks/<id>/edit/]
   └── ProdukUpdateView.post(request)
        └── ProdukService.update_produk(instance_id, form_data)
             └── Produk.objects.filter(pk=id).update(...)
  ```
* **Expected Metrics**: `execution_time: ~40ms`, `db_queries: 3`

#### D. Delete Entity (`DELETE /inventory/produks/<id>/delete/`)
* **View Class**: `ProdukDeleteView` (`apps.inventory.views.produk.ProdukDeleteView`)
* **Execution Path**:
  ```text
  [DELETE /inventory/produks/<id>/delete/]
   └── ProdukDeleteView.delete(request, pk)
        └── ProdukService.delete_produk(pk)
             └── Produk.objects.get(pk=pk).delete()
  ```
* **Expected Metrics**: `execution_time: ~30ms`, `db_queries: 2`

---

## 2. User Guide (Panduan Pengguna)

### Cara Mengelola Data Produk

1. **Melihat Daftar Data**:
   * Buka menu **"Produk"** pada sidebar dashboard.
   * Gunakan kotak pencarian untuk mencari berdasarkan nama/SKU atau gunakan dropdown filter.

2. **Menambah Data Baru**:
   * Klik tombol **"+ Tambah Produk"** di sudut kanan atas.
   * Isi form yang muncul pada modal dialog.
   * Klik **"Simpan"**. Data baru akan langsung muncul pada tabel.

3. **Mengubah / Edit Data**:
   * Klik ikon **Edit (Pensil)** pada baris data yang ingin diubah.
   * Perbarui informasi pada form modal, lalu klik **"Simpan Perubahan"**.

4. **Menghapus Data**:
   * Klik ikon **Hapus (Tong Sampah)** pada baris data.
   * Konfirmasi penghapusan pada dialog peringatan.

---

## 3. FAQ (Pertanyaan Umum)

**Q: Apakah data Produk yang sudah dihapus bisa dikembalikan?**  
*A: Data yang dihapus secara permanen tidak dapat dikembalikan. Namun log aktivitas historis tetap tersimpan dalam sistem audit history.*

**Q: Mengapa data baru yang saya tambahkan tidak langsung muncul?**  
*A: Pastikan koneksi internet Anda stabil. Jika menggunakan pencarian, hapus kata kunci pada kotak pencarian untuk melihat seluruh data.*

---

## 4. Help & Troubleshooting (Pesan Error & Solusi)

| Error Code | HTTP Status | Pesan Error UI | Penyebab & Solusi |
|---|---|---|---|
| `VALIDATION_ERROR` | 422 | "Data input tidak valid." | Ada field wajib yang kosong atau format tidak sesuai. Periksa kembali form input. |
| `PRODUK_NOT_FOUND` | 404 | "Data Produk tidak ditemukan." | Data mungkin telah dihapus oleh pengguna lain. Refresh halaman tabel. |
| `PERMISSION_DENIED` | 403 | "Anda tidak memiliki akses." | Peran akun Anda tidak memiliki izin mengedit/menghapus data ini. Hubungi admin. |
