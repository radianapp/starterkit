# SOP Pola Interaktivitas HTMX (HTMX Interaction Patterns)

Dokumen ini mendefinisikan standar operasional prosedur untuk mengimplementasikan interaktivitas frontend menggunakan **HTMX** di dalam ekosistem Radian Data Platform (RDP).

## 1. Prinsip Utama (HATEOAS)
- Frontend digerakkan sepenuhnya oleh HTML parsial yang dikembalikan oleh backend.
- Minimalkan penulisan Javascript kustom. Gunakan atribut HTMX bawaan untuk menangani transisi state.
- **Kombinasi dengan Alpine.js**: Gunakan Alpine.js untuk manipulasi DOM lokal yang murni berbasis visual (seperti membuka/menutup dropdown atau toggle tab lokal), dan gunakan HTMX untuk operasi yang membutuhkan data dari server.

---

## 2. Struktur Response & HTTP Status Codes

### A. HTTP 200 OK (Success dengan HTML Partial)
Digunakan saat request berhasil dan server mengembalikan fragmen HTML untuk di-render oleh client.
```python
# View Django
return render(request, "partials/item_row.html", {"item": item})
```

### B. HTTP 422 Unprocessable Entity (Validation Error)
Gunakan status **422** (bukan 200) untuk response yang berisi form dengan pesan error / validasi gagal. Hal ini memungkinkan HTMX (atau event handlers) mengetahui adanya error untuk memicu event visual (seperti toast/alert).
```python
# View Django
return render(request, "partials/form.html", {"form": form}, status=422)
```

### C. HX-Redirect (Redirect Penuh Halaman)
Jika alur setelah sukses memerlukan redirect penuh halaman (misal setelah login atau registrasi), jangan kembalikan status 302 standar Django (karena HTMX akan me-load halaman tujuan di dalam kontainer target). Sebagai gantinya, kirimkan header `HX-Redirect`:
```python
from django.http import HttpResponse

response = HttpResponse()
response["HX-Redirect"] = "/dashboard/"
return response
```

### D. HX-Trigger (Memicu Event Sisi Klien)
Gunakan header `HX-Trigger` untuk memicu event global di sisi browser, misalnya untuk menampilkan Toast Notification setelah berhasil melakukan aksi.
```python
import json
from django.http import HttpResponse

response = HttpResponse("Aksi berhasil dilakukan!")
response["HX-Trigger"] = json.dumps({
    "showToast": {
        "message": "Data berhasil disimpan!",
        "tags": "success"
    }
})
return response
```

---

## 3. Contoh Pola Implementasi (HTMX Patterns)

### A. Inline Edit (Sunting Langsung)
Mengganti teks dinamis dengan form edit tanpa memuat ulang halaman.
```html
{# templates/htmx_examples/inline_edit.html #}
<div id="contact-info" hx-target="this" hx-swap="outerHTML">
    <p>Nama: {{ contact.name }}</p>
    <button hx-get="{% url 'contacts:edit' contact.id %}">Sunting</button>
</div>
```

### B. Delete Confirm (Konfirmasi Hapus)
Menampilkan konfirmasi hapus data secara asinkronus menggunakan event handler global atau modal dialog.
```html
<button 
    hx-delete="{% url 'items:delete' item.id %}"
    hx-confirm="Apakah Anda yakin ingin menghapus data ini?"
    hx-target="#item-row-{{ item.id }}"
    hx-swap="outerHTML">
    Hapus
</button>
```

---

## 4. Keamanan (CSRF Protection)
Semua request non-GET (POST, PUT, DELETE) melalui HTMX **wajib** menyertakan token CSRF. starter kit secara global menangani ini dengan mendengarkan event `htmx:configRequest` di file base layout:
```javascript
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
```
Namun, jika dideklarasikan manual pada element, gunakan:
```html
<button hx-post="{% url 'action' %}" hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    Kirim
</button>
```
