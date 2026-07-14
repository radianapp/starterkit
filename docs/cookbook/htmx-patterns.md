# Cookbook: Pola Interaktivitas HTMX di RDP Starter Kit

Dokumen ini berisi panduan langkah-demi-langkah (resep) untuk mengimplementasikan 10 pola interaktivitas HTMX yang umum digunakan di platform RDP.

---

## 1. Validasi Form dengan HTTP 422 & HX-Redirect
**Tujuan**: Menangani form error tanpa full-page reload. Mengembalikan potongan HTML form yang berisi error dari server jika form tidak valid, dan mengalihkan halaman menggunakan header `HX-Redirect` jika form sukses diproses.

### Kode View (Django)
```python
# Menggunakan HtmxFormMixin yang otomatis mengembalikan status 422 jika invalid
from django.views.generic import FormView
from apps.core.mixins.htmx import HtmxFormMixin

class ContactCreateView(HtmxFormMixin, FormView):
    form_class = ContactForm
    template_name = "contact_form.html"
    success_url = "/success/"
```

### Kode Template (HTML)
```html
<form hx-post="{% url 'contact-create' %}" hx-target="#contact-form-container" hx-swap="outerHTML">
    <!-- input fields dan error tags -->
</form>
```

---

## 2. Modal Form
**Tujuan**: Membuka form di dalam modal dialog secara dinamis dan menutupnya setelah sukses.

### Kode Template (HTML)
```html
<dialog id="contact-modal" class="rdp-modal">
    <article>
        <header>
            <button onclick="document.getElementById('contact-modal').close()">&times;</button>
            <h3>Kontak Baru</h3>
        </header>
        <div id="contact-modal-body">
            <!-- Form HTMX di-load di sini -->
        </div>
    </article>
</dialog>
```

---

## 3. Delete Confirmation
**Tujuan**: Menghapus item baris data dengan konfirmasi bawaan browser sebelum request dikirimkan ke server.

### Kode Template (HTML)
```html
<button hx-delete="{% url 'contact-delete' pk=contact.id %}" 
        hx-confirm="Apakah Anda yakin ingin menghapus kontak ini?" 
        hx-target="#contact-row-{{ contact.id }}" 
        hx-swap="outerHTML">
    Hapus
</button>
```

---

## 4. Live Validation Field
**Tujuan**: Memvalidasi input tertentu (seperti email unik) secara real-time saat pengguna mengetik dengan debounce agar tidak membebani server.

### Kode Template (HTML)
```html
<input type="email" 
       name="email" 
       hx-post="{% url 'live-validation' %}" 
       hx-trigger="keyup changed delay:400ms" 
       hx-target="#email-validation-wrapper" 
       hx-swap="outerHTML" />
```

---

## 5. Inline Edit
**Tujuan**: Mengubah baris tabel atau item data secara langsung di tempat tanpa membuka halaman baru.

### Kode Template (HTML)
```html
<!-- Baris View Mode -->
<tr id="row-{{ item.id }}">
    <td>{{ item.name }}</td>
    <button hx-get="{% url 'item-edit' pk=item.id %}" hx-target="#row-{{ item.id }}" hx-swap="outerHTML">Edit</button>
</tr>

<!-- Baris Edit Mode (Returned dari server) -->
<tr id="row-{{ item.id }}">
    <td><input type="text" name="name" value="{{ item.name }}" /></td>
    <button hx-post="{% url 'item-edit' pk=item.id %}" hx-include="closest tr" hx-target="#row-{{ item.id }}" hx-swap="outerHTML">Simpan</button>
</tr>
```

---

## 6. Live Search dengan Debounce
**Tujuan**: Menyaring baris data tabel secara real-time dari server saat pengguna mengetik di input search box.

### Kode Template (HTML)
```html
<input type="search" 
       name="q" 
       placeholder="Cari..." 
       hx-get="{% url 'contact-search' %}" 
       hx-trigger="keyup changed delay:300ms, search" 
       hx-target="#contact-list-body" />
```

---

## 7. Pagination Fragment
**Tujuan**: Berpindah halaman tabel secara dinamis dengan hanya memperbarui area tabel data, bukan memuat ulang seluruh halaman web.

### Kode Template (HTML)
```html
<!-- Menggunakan komponen c-rdp.pagination bawaan -->
<c-rdp.pagination page_obj="{{ page_obj }}" url_pattern="/dashboard/?page=" />
```

---

## 8. Infinite Scroll
**Tujuan**: Memuat baris log atau data tambahan secara otomatis saat pengguna men-scroll halaman sampai bawah.

### Kode Template (HTML)
```html
{% for row in rows %}
    <tr>
        <td>{{ row.title }}</td>
    </tr>
    {% if forloop.last and next_page %}
        <tr hx-get="{% url 'infinite-scroll-rows' %}?page={{ next_page }}"
            hx-trigger="revealed"
            hx-swap="afterend"
            hx-target="this">
            <td colspan="3">Memuat log lainnya...</td>
        </tr>
    {% endif %}
{% endfor %}
```

---

## 9. Polling Status
**Tujuan**: Memperbarui status progress job atau data dashboard dari server secara berkala setiap N detik.

### Kode Template (HTML)
```html
<div hx-get="{% url 'polling' %}" hx-trigger="every 2s" hx-target="this" hx-swap="outerHTML">
    Progress saat ini: {{ progress }}%
</div>
```

---

## 10. Toast Notification via Header `HX-Trigger`
**Tujuan**: Memicu toast notification di browser setelah server berhasil memproses request tertentu dengan menyertakan custom JSON header `HX-Trigger`.

### Kode View (Django)
```python
import json
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse("Sukses!")
    response["HX-Trigger"] = json.dumps({
        "showToast": {
            "message": "Operasi berhasil diselesaikan!",
            "type": "success"
        }
    })
    return response
```
