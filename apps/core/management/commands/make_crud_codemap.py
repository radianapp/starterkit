"""
Django Management Command: make_crud_codemap
---------------------------------------------
Membuat secara otomatis dokumen Code Map, User Guide, FAQ, dan Help untuk modul CRUD.

Usage:
    python manage.py make_crud_codemap <app_label> <model_name>

Contoh:
    python manage.py make_crud_codemap inventory Produk
"""

import subprocess
import sys
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate Code Map, User Guide, FAQ, dan Help otomatis untuk modul CRUD."

    def add_arguments(self, parser):
        parser.add_argument("app_label", type=str, help="Nama app Django (misal: inventory)")
        parser.add_argument("model_name", type=str, help="Nama Model Django (misal: Produk)")

    def handle(self, *args, **options):
        app_label = options["app_label"].lower()
        model_name = options["model_name"]

        try:
            model_cls = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f"Model '{model_name}' tidak ditemukan di app '{app_label}'.")

        verbose_name = getattr(model_cls._meta, "verbose_name_plural", model_name).title()
        model_slug = model_name.lower()

        # Determine paths
        base_dir = Path(apps.get_app_config(app_label).path).parent.parent
        codemap_dir = base_dir / "docs" / "codemap" / app_label
        codemap_dir.mkdir(parents=True, exist_ok=True)
        doc_file = codemap_dir / f"{model_slug}-crud.md"

        # Inspect model fields
        fields_summary = []
        for field in model_cls._meta.get_fields():
            if hasattr(field, "column"):
                fields_summary.append(f"`{field.name}` ({field.get_internal_type()})")

        fields_str = ", ".join(fields_summary)

        content = f"""# Code Map & Docs: {verbose_name} CRUD Management

**App Domain**: `{app_label}`  
**Event Category**: `CRUD Management`  
**User Story Ref**: `US-CRUD-{model_name.upper()}`

---

## 1. Developer View (Code Map & Tracing)

Pemetaan alur eksekusi lengkap untuk operasi CRUD pada entity **{model_name}**.

### Model Attributes & Fields
* **Model Class**: `apps.{app_label}.models.{model_name}`
* **Table Name**: `{model_cls._meta.db_table}`
* **Fields**: {fields_str}

---

### Operations Breakdown

#### A. Read / List & Search (`GET /{app_label}/{model_slug}s/`)
* **View Class**: `{model_name}ListView` (`apps.{app_label}.views.{model_slug}.{model_name}ListView`)
* **Execution Path**:
  ```text
  [GET /{app_label}/{model_slug}s/]
   └── {model_name}ListView.get(request)
        └── {model_name}Service.get_paginated_list(search_query, filter_params)
             └── {model_name}.objects.filter(...).select_related(...)
  ```
* **Expected Metrics**: `execution_time: ~20ms`, `db_queries: 2`

#### B. Create / Add Entity (`POST /{app_label}/{model_slug}s/create/`)
* **View Class**: `{model_name}CreateView` (`apps.{app_label}.views.{model_slug}.{model_name}CreateView`)
* **Execution Path**:
  ```text
  [POST /{app_label}/{model_slug}s/create/]
   └── {model_name}CreateView.post(request)
        └── {model_name}Service.create_{model_slug}(form_data)
             ├── {model_name}Form.is_valid()
             └── {model_name}.objects.create(...)
  ```
* **Expected Metrics**: `execution_time: ~45ms`, `db_queries: 3`

#### C. Update / Edit Entity (`POST /{app_label}/{model_slug}s/<id>/edit/`)
* **View Class**: `{model_name}UpdateView` (`apps.{app_label}.views.{model_slug}.{model_name}UpdateView`)
* **Execution Path**:
  ```text
  [POST /{app_label}/{model_slug}s/<id>/edit/]
   └── {model_name}UpdateView.post(request)
        └── {model_name}Service.update_{model_slug}(instance_id, form_data)
             └── {model_name}.objects.filter(pk=id).update(...)
  ```
* **Expected Metrics**: `execution_time: ~40ms`, `db_queries: 3`

#### D. Delete Entity (`DELETE /{app_label}/{model_slug}s/<id>/delete/`)
* **View Class**: `{model_name}DeleteView` (`apps.{app_label}.views.{model_slug}.{model_name}DeleteView`)
* **Execution Path**:
  ```text
  [DELETE /{app_label}/{model_slug}s/<id>/delete/]
   └── {model_name}DeleteView.delete(request, pk)
        └── {model_name}Service.delete_{model_slug}(pk)
             └── {model_name}.objects.get(pk=pk).delete()
  ```
* **Expected Metrics**: `execution_time: ~30ms`, `db_queries: 2`

---

## 2. User Guide (Panduan Pengguna)

### Cara Mengelola Data {verbose_name}

1. **Melihat Daftar Data**:
   * Buka menu **"{verbose_name}"** pada sidebar dashboard.
   * Gunakan kotak pencarian untuk mencari berdasarkan nama/SKU atau gunakan dropdown filter.

2. **Menambah Data Baru**:
   * Klik tombol **"+ Tambah {model_name}"** di sudut kanan atas.
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

**Q: Apakah data {model_name} yang sudah dihapus bisa dikembalikan?**  
*A: Data yang dihapus secara permanen tidak dapat dikembalikan. Namun log aktivitas historis tetap tersimpan dalam sistem audit history.*

**Q: Mengapa data baru yang saya tambahkan tidak langsung muncul?**  
*A: Pastikan koneksi internet Anda stabil. Jika menggunakan pencarian, hapus kata kunci pada kotak pencarian untuk melihat seluruh data.*

---

## 4. Help & Troubleshooting (Pesan Error & Solusi)

| Error Code | HTTP Status | Pesan Error UI | Penyebab & Solusi |
|---|---|---|---|
| `VALIDATION_ERROR` | 422 | "Data input tidak valid." | Ada field wajib yang kosong atau format tidak sesuai. Periksa kembali form input. |
| `{model_name.upper()}_NOT_FOUND` | 404 | "Data {model_name} tidak ditemukan." | Data mungkin telah dihapus oleh pengguna lain. Refresh halaman tabel. |
| `PERMISSION_DENIED` | 403 | "Anda tidak memiliki akses." | Peran akun Anda tidak memiliki izin mengedit/menghapus data ini. Hubungi admin. |
"""

        doc_file.write_text(content.strip() + "\n", encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"[OK] Document generated: {doc_file}"))

        # Re-run index generator
        index_script = base_dir / "scripts" / "generate_docs_index.py"
        if index_script.exists():
            subprocess.run([sys.executable, str(index_script)], check=False)
            self.stdout.write(self.style.SUCCESS("[OK] Auto-updated master INDEX.md"))
