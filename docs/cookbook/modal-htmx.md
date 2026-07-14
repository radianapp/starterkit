# Cookbook: Dynamic Forms dalam Modal Menggunakan HTMX

Resep ini menjelaskan bagaimana memuat form dinamis ke dalam modal global dan memproses pengiriman data form secara asinkron menggunakan HTMX.

---

## Langkah 1: Siapkan Kontainer Modal Global
Pastikan base layout (misalnya di `templates/cotton/layout/dashboard.html` atau sejenisnya) memiliki elemen modal global kosong yang dikendalikan oleh Alpine.js atau CSS dialog PicoCSS:

```html
<!-- Modal Container Global -->
<dialog id="global-modal" class="modal">
    <article>
        <header>
            <a href="#close" aria-label="Close" class="close" onclick="document.getElementById('global-modal').removeAttribute('open')"></a>
            <h5 id="modal-title">Form Data</h5>
        </header>
        <div id="modal-content">
            <!-- Form dinamis akan dimuat di sini oleh HTMX -->
        </div>
    </article>
</dialog>
```

---

## Langkah 2: Pemicu HTMX untuk Membuka Modal
Pada tombol "Tambah" atau "Edit", buat request GET HTMX untuk mengambil konten form dan memasukkannya ke dalam kontainer modal, lalu buka dialog modal.

```html
<button 
    hx-get="{% url 'books:create' %}" 
    hx-target="#modal-content"
    hx-trigger="click"
    onclick="document.getElementById('global-modal').setAttribute('open', 'true')">
    Tambah Buku Baru
</button>
```

---

## Langkah 3: Layout Form Parsial di Sisi Server
Template form parsial (`templates/books/partials/book_form.html`) harus memiliki target pengiriman form yang spesifik. Jika berhasil, kita tutup modal dan update data daftar:

```html
<form hx-post="{% url 'books:create' %}" hx-target="#book-list" hx-swap="beforeend">
    {% csrf_token %}
    {{ form.as_p }}
    
    <footer>
        <button type="button" class="secondary" onclick="document.getElementById('global-modal').removeAttribute('open')">Batal</button>
        <button type="submit">Simpan</button>
    </footer>
</form>
```

---

## Langkah 4: Handling Response Berhasil di View
Pada backend, setelah data berhasil disimpan, kembalikan baris HTML baru dan sertakan header `HX-Trigger` untuk menutup modal secara otomatis jika diinginkan, atau biarkan penutupan modal ditangani oleh event listener client-side.

```python
# Django View
def post(self, request):
    form = BookForm(request.POST)
    if form.is_valid():
        book = form.save()
        response = render(request, "books/partials/book_row.html", {"book": book})
        # Trigger penutupan modal di sisi client
        response["HX-Trigger"] = "closeModal"
        return response
    return render(request, "books/partials/book_form.html", {"form": form}, status=422)
```

Di javascript global (`static/js/modal-global.js`):
```javascript
document.body.addEventListener("closeModal", function() {
    document.getElementById("global-modal").removeAttribute("open");
});
```
